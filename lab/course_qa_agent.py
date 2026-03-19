import argparse
import asyncio
import os
import re
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient


ROOT_DIR = Path(__file__).resolve().parents[1]

DEFAULT_DOC_PATHS = [
    ROOT_DIR / "translations/zh-CN/02-explore-agentic-frameworks/README.md",
    ROOT_DIR / "translations/zh-CN/03-agentic-design-patterns/README.md",
    ROOT_DIR / "translations/zh-CN/04-tool-use/README.md",
    ROOT_DIR / "translations/zh-CN/02-explore-agentic-frameworks/azure-ai-foundry-agent-creation.md",
]

AGENT_NAME = "CourseQAAgent"
AGENT_INSTRUCTIONS = """
你是一个课程资料问答 Agent，负责回答与 AI Agent、Agent Framework、Design Pattern、Tool Use、
Azure AI Foundry 相关的问题。

回答要求：
1. 回答前优先调用检索工具，先找到和问题最相关的课程资料。
2. 只基于检索到的上下文回答，不要编造课程里没有的信息。
3. 回答尽量简洁清楚，适合组会汇报和学习场景。
4. 回答结尾请给出“来源”一行，列出你实际使用到的文件名。
5. 如果资料不足以支撑结论，请明确说明“当前资料不足以完全回答这个问题”。
""".strip()

REQUIRED_ENV_VARS = ["GITHUB_TOKEN", "GITHUB_ENDPOINT", "GITHUB_MODEL_ID"]
STOPWORDS = {
    "什么",
    "怎么",
    "如何",
    "一个",
    "一些",
    "这个",
    "那个",
    "哪些",
    "以及",
    "我们",
    "你们",
    "他们",
    "可以",
    "进行",
    "使用",
    "有关",
    "关于",
    "一下",
    "一下子",
    "请问",
    "是否",
    "需要",
    "为什么",
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "into",
    "what",
    "how",
    "why",
}


@dataclass
class Chunk:
    source: str
    section: str
    content: str
    search_text: str


def clean_text(text: str) -> str:
    text = text.replace("\ufeff", " ").replace("\u3000", " ")
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"`{3}.*?`{3}", " ", text, flags=re.S)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_terms(query: str) -> list[str]:
    normalized = clean_text(query).lower()
    english_terms = [
        term
        for term in re.findall(r"[a-z0-9][a-z0-9_-]{1,}", normalized)
        if term not in STOPWORDS
    ]

    chinese_terms: list[str] = []
    for segment in re.findall(r"[\u4e00-\u9fff]{2,}", normalized):
        if segment not in STOPWORDS:
            chinese_terms.append(segment)
        for window in (2, 3):
            if len(segment) >= window:
                for index in range(len(segment) - window + 1):
                    term = segment[index : index + window]
                    if term not in STOPWORDS:
                        chinese_terms.append(term)

    seen: set[str] = set()
    ordered_terms: list[str] = []
    for term in english_terms + chinese_terms:
        if term not in seen:
            seen.add(term)
            ordered_terms.append(term)
    return ordered_terms


def iter_markdown_chunks(text: str) -> list[tuple[str, str]]:
    chunks: list[tuple[str, str]] = []
    current_section = "Overview"
    buffer: list[str] = []

    def flush() -> None:
        content = clean_text("\n".join(buffer))
        if len(content) >= 80:
            chunks.append((current_section, content))
        buffer.clear()

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.lstrip().startswith("#"):
            flush()
            current_section = clean_text(line.lstrip("#").strip()) or current_section
            continue
        if line.strip() == "":
            flush()
            continue
        buffer.append(line)

    flush()
    return chunks


def load_corpus(doc_paths: list[Path]) -> list[Chunk]:
    corpus: list[Chunk] = []
    for path in doc_paths:
        if not path.exists():
            continue
        raw_text = path.read_text(encoding="utf-8")
        for section, content in iter_markdown_chunks(raw_text):
            search_text = f"{section} {content}".lower()
            corpus.append(
                Chunk(
                    source=str(path.relative_to(ROOT_DIR)).replace("\\", "/"),
                    section=section,
                    content=content,
                    search_text=search_text,
                )
            )
    return corpus


CORPUS = load_corpus(DEFAULT_DOC_PATHS)


def score_chunk(query: str, chunk: Chunk) -> int:
    query_text = clean_text(query).lower()
    terms = extract_terms(query)
    score = 0

    if query_text and query_text in chunk.search_text:
        score += 12

    for term in terms:
        if term in chunk.search_text:
            if len(term) >= 4:
                score += 4
            elif len(term) == 3:
                score += 3
            else:
                score += 2

            if term in chunk.section.lower():
                score += 2

    return score


def retrieve_top_chunks(query: str, top_k: int = 3) -> list[Chunk]:
    ranked = sorted(
        ((score_chunk(query, chunk), chunk) for chunk in CORPUS),
        key=lambda item: item[0],
        reverse=True,
    )
    return [chunk for score, chunk in ranked if score > 0][:top_k]


def retrieve_course_context(query: str, top_k: int = 3) -> str:
    """Retrieve the most relevant course context for a user question."""
    matches = retrieve_top_chunks(query, top_k=top_k)
    if not matches:
        return "No relevant context found in the selected course materials."

    sections = []
    for index, match in enumerate(matches, start=1):
        sections.append(
            f"[Context {index}]\n"
            f"Source: {match.source}\n"
            f"Section: {match.section}\n"
            f"Content: {match.content}"
        )
    return "\n\n".join(sections)


def list_available_sources() -> str:
    """List the course files that this agent can search."""
    return "\n".join(f"- {path.relative_to(ROOT_DIR)}" for path in DEFAULT_DOC_PATHS if path.exists())


def preview_retrieval(query: str, top_k: int = 3) -> str:
    matches = retrieve_top_chunks(query, top_k=top_k)
    if not matches:
        return "No local matches found."
    blocks = []
    for index, match in enumerate(matches, start=1):
        blocks.append(
            f"[Top {index}] {match.source} | {match.section}\n"
            f"{match.content}"
        )
    return "\n\n".join(blocks)


def create_agent() -> Agent:
    load_dotenv()
    missing = [key for key in REQUIRED_ENV_VARS if not os.getenv(key)]
    if missing:
        missing_text = ", ".join(missing)
        raise SystemExit(
            f"Missing environment variables: {missing_text}\n"
            "Please update your .env file before running the agent."
        )

    client = OpenAIChatClient(
        base_url=os.environ["GITHUB_ENDPOINT"],
        api_key=os.environ["GITHUB_TOKEN"],
        model_id=os.environ["GITHUB_MODEL_ID"],
    )

    return Agent(
        name=AGENT_NAME,
        client=client,
        instructions=AGENT_INSTRUCTIONS,
        tools=[retrieve_course_context, list_available_sources],
    )


def extract_text_from_response(response) -> str:
    for message in reversed(getattr(response, "messages", [])):
        contents = getattr(message, "contents", None) or []
        text_parts = [getattr(content, "text", "") for content in contents if getattr(content, "text", "")]
        if text_parts:
            return "\n".join(text_parts).strip()
    return str(response)


def format_agent_error(exc: Exception) -> str:
    return (
        "Agent request failed.\n"
        f"Reason: {exc}\n"
        "Please check your network connection and GITHUB_* environment variables.\n"
        "If you only want to verify local retrieval, run the script with --preview."
    )


async def run_single_query(query: str, show_context: bool) -> str:
    if show_context:
        print("=== Retrieved Context Preview ===")
        print(preview_retrieval(query))
        print()

    agent = create_agent()
    session = agent.create_session()
    try:
        response = await agent.run(query, session=session)
    except Exception as exc:
        raise SystemExit(format_agent_error(exc)) from exc
    return extract_text_from_response(response)


async def run_interactive(show_context: bool) -> None:
    agent = create_agent()
    session = agent.create_session()

    print("CourseQAAgent is ready. Type your question below.")
    print("Type exit to stop.\n")

    while True:
        query = input("Question> ").strip()
        if not query:
            continue
        if query.lower() in {"exit", "quit", "q"}:
            print("Session ended.")
            return

        if show_context:
            print("\n=== Retrieved Context Preview ===")
            print(preview_retrieval(query))
            print()

        try:
            response = await agent.run(query, session=session)
        except Exception as exc:
            print(format_agent_error(exc))
            print()
            continue
        print("=== Agent Answer ===")
        print(extract_text_from_response(response))
        print()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Minimal course-material QA agent for lab demos.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--query", help="Ask one question and print the model answer.")
    group.add_argument("--preview", help="Preview the locally retrieved chunks without calling the model.")
    parser.add_argument(
        "--show-context",
        action="store_true",
        help="Show the retrieved chunks before asking the model.",
    )
    return parser.parse_args()


async def main() -> None:
    args = parse_args()

    if not CORPUS:
        raise SystemExit("No course materials were loaded. Please check the default document paths.")

    if args.preview:
        print(preview_retrieval(args.preview))
        return

    if args.query:
        answer = await run_single_query(args.query, show_context=args.show_context)
        print(answer)
        return

    await run_interactive(show_context=args.show_context)


if __name__ == "__main__":
    asyncio.run(main())

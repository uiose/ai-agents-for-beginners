# CourseQAAgent Architecture

这个最小 Agent 可以按经典智能体视角拆成 4 层：

- 环境：用户、课程资料、`.env` 配置、外部模型服务
- 传感器：接收问题、读取本地资料、感知可用配置
- 决策器：根据系统指令决定是否检索、如何组织回答
- 执行器：调用工具、请求模型、把结果输出给用户

## 1. 智能体分层架构图

```mermaid
flowchart LR
    subgraph ENV["环境 Environment"]
        U["用户 / 命令行"]
        D["课程资料 Markdown\nDEFAULT_DOC_PATHS"]
        C[".env 配置\nGITHUB_*"]
        M["GitHub Models / OpenAI-compatible Endpoint"]
    end

    subgraph SENSE["传感器 Sensors"]
        S1["输入感知\nparse_args()\ninput()"]
        S2["资料感知\nload_corpus()\nCORPUS"]
        S3["上下文感知\nretrieve_top_chunks()\nscore_chunk()"]
        S4["配置感知\nload_dotenv()\nos.getenv()"]
    end

    subgraph DECIDE["决策器 Controller / Brain"]
        B1["Agent\nname + tools + session"]
        B2["系统策略\nAGENT_INSTRUCTIONS"]
        B3["回答编排\n是否调用检索工具\n是否给出来源"]
    end

    subgraph ACT["执行器 Actuators"]
        A1["工具执行\nretrieve_course_context()\nlist_available_sources()"]
        A2["模型调用\nOpenAIChatClient"]
        A3["结果输出\nprint()\nextract_text_from_response()"]
    end

    U --> S1
    D --> S2
    D --> S3
    C --> S4

    S1 --> B1
    S2 --> B1
    S3 --> B3
    S4 --> B1
    B2 --> B1
    B1 --> B3

    B3 --> A1
    B3 --> A2
    A1 --> B1
    A2 --> B1
    B1 --> A3
    A3 --> U
    A2 --> M
```

## 2. 一次问答的执行流

```mermaid
sequenceDiagram
    participant User as 用户
    participant CLI as CLI输入层
    participant Agent as Agent控制器
    participant Tool as 检索工具
    participant Corpus as 本地语料库 CORPUS
    participant LLM as OpenAIChatClient
    participant Terminal as 终端输出

    User->>CLI: 输入问题 / --query / --preview
    CLI->>Agent: 传入 query

    alt 仅预览检索结果
        Agent->>Tool: preview_retrieval(query)
        Tool->>Corpus: retrieve_top_chunks(query)
        Corpus-->>Tool: top_k chunks
        Tool-->>Terminal: 输出检索片段
        Terminal-->>User: 显示本地命中内容
    else 正常问答
        Agent->>Tool: retrieve_course_context(query)
        Tool->>Corpus: score_chunk + 排序
        Corpus-->>Tool: top_k chunks
        Tool-->>Agent: 拼接后的 context
        Agent->>LLM: instructions + query + context + session
        LLM-->>Agent: 回答 / 工具调用结果
        Agent->>Terminal: extract_text_from_response()
        Terminal-->>User: 显示最终答案
    end
```

## 3. 代码到架构角色的映射

| 架构角色 | 对应实现 | 说明 |
| --- | --- | --- |
| 环境 | `DEFAULT_DOC_PATHS`、`.env`、用户输入、模型服务 | Agent 运行时依赖的外部世界 |
| 传感器 | `parse_args()`、`input()`、`load_corpus()`、`retrieve_top_chunks()` | 负责感知问题、资料和配置 |
| 决策器 | `Agent(...)`、`AGENT_INSTRUCTIONS`、`session` | 决定先检索还是直接答、如何输出 |
| 执行器 | `retrieve_course_context()`、`list_available_sources()`、`OpenAIChatClient`、`print()` | 把决策转成具体动作 |

## 4. 你汇报时可以直接这样讲

可以把这个最小 Agent 概括成一句话：

> 它先通过“传感器”感知用户问题和本地课程资料，再由 Agent 决策器判断是否调用检索工具，最后通过执行器去调用模型并把答案返回给用户。

如果老师追问它是不是“闭环”，更准确的说法是：

> 严格来说，它更接近开环问答系统：接收问题后检索资料并生成答案，但输出后不会再观察答案效果，也不会基于环境反馈自动修正。

不过在单次问答内部，它有一个局部反馈链路：

> Agent 可以先调用检索工具拿到 context，再基于这个返回结果继续生成回答，所以它不是完全无反馈，但还不是带外部结果校正的完整闭环。

# Lab: 课程资料问答 Agent

这个 `lab` 目录里放的是一个适合明天组会汇报的最小原型：单 Agent、基于课程资料的本地检索增强问答、带简单工具调用。

## 你可以怎么介绍它

- 题目：我在做一个面向课程资料和技术文档的问答辅助 Agent，用来帮助用户快速获取准确且可追溯的信息。
- 输入输出：输入是用户提出的问题，输出是结合相关资料生成的回答，并给出对应的依据或来源。
- 技术路线：基于大语言模型，结合本地检索增强和简单工具调用，使用 Microsoft Agent Framework 搭建一个可运行的单 Agent 原型。

## 当前文件

- `course_qa_agent.py`：主脚本，包含 Agent、检索工具、交互式问答。
- `course_qa_agent_architecture.md`：按“环境 / 传感器 / 决策器 / 执行器”整理的架构图和执行流。

## 当前知识库范围

脚本默认检索这些课程资料：

- `translations/zh-CN/02-explore-agentic-frameworks/README.md`
- `translations/zh-CN/03-agentic-design-patterns/README.md`
- `translations/zh-CN/04-tool-use/README.md`
- `translations/zh-CN/02-explore-agentic-frameworks/azure-ai-foundry-agent-creation.md`

这个范围是故意收缩过的，优先保证明天能讲清楚、能跑通、能看到结果。

## 运行方式

先确认 `.env` 里至少有这些变量：

```env
GITHUB_TOKEN=...
GITHUB_ENDPOINT=https://models.inference.ai.azure.com
GITHUB_MODEL_ID=gpt-4o-mini
```

预览本地检索结果，不调用模型：

```powershell
.\venv\Scripts\python .\lab\course_qa_agent.py --preview "什么是工具使用设计模式？"
```

跑单次问答：

```powershell
.\venv\Scripts\python .\lab\course_qa_agent.py --query "Microsoft Agent Framework 和 Azure AI Agent Service 有什么区别？"
```

查看检索上下文再问答：

```powershell
.\venv\Scripts\python .\lab\course_qa_agent.py --query "什么是 agentic framework？" --show-context
```

进入交互模式：

```powershell
.\venv\Scripts\python .\lab\course_qa_agent.py
```

## 这个原型做了什么

- 用 `Agent Framework` 创建单 Agent。
- 用 `retrieve_course_context()` 作为检索工具，从本地课程资料里找最相关的段落。
- 用 `list_available_sources()` 作为简单工具，让 Agent 知道自己能查哪些文件。
- 要求 Agent 只基于检索结果回答，并在结尾给出来源。

## 为什么我先这样做

- 风险低：不依赖 Azure Search 索引搭建，今晚就能先出结果。
- 可汇报：已经具备“问题定义-方法-初步结果-下一步”的完整链路。
- 好扩展：后面可以把本地检索替换成 Azure AI Search，升级成更标准的 RAG。

## 明天组会可以怎么说

你可以直接按这个逻辑说：

1. 我先把目标收缩成“课程资料问答”这个单任务 Agent，而不是一开始就做通用多 Agent 系统。
2. 当前已经完成了一个最小可运行原型，能从课程资料中检索相关内容，并生成带来源的回答。
3. 目前优先验证的是基本链路是否跑通，以及检索结果能否支撑回答。严格来说，这个原型更接近开环问答，还不是带外部反馈校正的完整闭环。
4. 下一步会把本地检索升级成 Azure AI Search 或更标准的 RAG 流程，并补充评测样例。

## 下一步建议

- 跑 3 到 5 个问题，截屏保留输入输出。
- 记录 1 到 2 个成功案例。
- 记录 1 个失败案例，比如检索不准、来源不够、回答过于泛化。
- 汇报时重点讲“我已经验证了最小可运行链路，也识别出它目前还不是完整闭环”。

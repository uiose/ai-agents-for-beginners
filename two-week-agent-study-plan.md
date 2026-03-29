# Two-Week Agent 入门实战 Todo（从 ch04 开始）

适用人群：你当前已到 ch04，希望 14 天完成入门并做出可展示项目。  
学习强度：每天 5 小时（建议 2 小时学习 + 2.5 小时动手 + 0.5 小时复盘）。

## 总目标

1. 两周内完成课程主线（ch04 到 ch15 的核心内容）。
2. 做出 1 个可演示的 Agent 项目（建议基于 `lab/course_qa_agent.py` 迭代）。
3. 形成你自己的 Agent 入门工程套路（架构、调试、评测、复盘模板）。

## 项目主线（建议）

项目名：Course Copilot Agent（课程问答 + 工具调用 + 基础规划 + 记忆扩展）

阶段目标：
- Week 1：先做“能跑通”的 v0.1（单 Agent + 本地检索 + 来源引用）
- Week 2：再做“更像产品”的 v0.2（可靠性、可观测、协议/浏览器工具、最小评测）

## GitHub 动手参考池（优先借鉴，不追求完整复刻）

- microsoft/agent-framework：对齐本课程框架能力与工作流设计
- crewAIInc/crewAI：学习角色拆分、多 Agent 协作思路
- openai/openai-agents-python：学习轻量编排和多 Agent 结构
- bytedance/deer-flow：学习长任务流程、记忆与子任务调度思想
- langgenius/dify：学习工作流、知识库、可视化编排产品形态
- onyx-dot-app/onyx、1Panel-dev/MaxKB、eosphoros-ai/DB-GPT：学习企业知识问答/RAG 结构
- firecrawl/firecrawl：学习网页数据采集与 markdown 化输入思路（用于 ch15 扩展）

---

## Day 1（ch04 强化 + 工具调用实战）

### Focus
- 把“Tool Use 设计模式”从会看样例，变成能独立写一个最小工具链。

### Scheduled
- [ ] 45 分钟：复盘 ch04 核心概念，写 1 页笔记（tool schema、参数约束、调用回路）。
- [ ] 60 分钟：通读并运行 `lab/faq_agent_starter.py`，确认当前可运行基线。
- [ ] 90 分钟：新增 1 个工具（如 `summarize_lesson_points` 或 `search_glossary`）。
- [ ] 45 分钟：给工具调用链加日志（输入参数、输出摘要、耗时）。
- [ ] 30 分钟：设计 5 条测试问题，覆盖“应调用工具/不应调用工具”两类。
- [ ] 30 分钟：跑测并记录 2 个成功、1 个失败案例。
- [ ] 30 分钟：阅读 `openai/openai-agents-python` 中工具调用示例，写 3 条可迁移点。

### Someday
- [ ] 把工具返回结构统一成 JSON schema，方便后面做评测。
- [ ] 增加“工具失败重试”与“参数兜底默认值”。

---

## Day 2（ch05 RAG）

### Focus
- 完成“可引用来源”的本地 RAG 问答闭环。

### Scheduled
- [ ] 60 分钟：学习 ch05，整理 RAG 4 步（切分、检索、注入、生成）。
- [ ] 90 分钟：在 `lab/course_qa_agent.py` 中调整检索逻辑（TopK、分段长度、排序）。
- [ ] 60 分钟：实现回答末尾强制附“来源文件 + 段落摘要”。
- [ ] 45 分钟：构造 8 个问答样本，记录命中率与幻觉情况。
- [ ] 45 分钟：对比 `onyx-dot-app/onyx` 或 `MaxKB` 的知识库流程，写 5 条改进想法。
- [ ] 30 分钟：把今天结果沉淀到 `lab/` 下一份 `rag_eval_notes.md`。

### Someday
- [ ] 尝试接入向量库（FAISS/Chroma）替换当前简化检索。
- [ ] 为每条回答输出“证据置信度”。

---

## Day 3（ch06 可信 Agent）

### Focus
- 建立“拒答、澄清、引用”的安全与可信输出规则。

### Scheduled
- [ ] 60 分钟：学习 ch06，整理可信维度（安全、可解释、可控）。
- [ ] 60 分钟：写一版 system prompt 规范（越权问题拒答、信息不足先澄清）。
- [ ] 90 分钟：给主项目加 3 条 guardrails（来源不足不回答、敏感请求拒绝、越权拦截）。
- [ ] 45 分钟：做 6 条对抗式问题测试（诱导、越权、模糊问题）。
- [ ] 45 分钟：参考 `dify` 的工作流防护思想，写“输入过滤 + 输出约束”清单。
- [ ] 30 分钟：整理 `trustworthy_checklist.md`。

### Someday
- [ ] 增加可配置策略文件（不同场景切换不同风控等级）。
- [ ] 给拒答增加“可执行替代建议”。

---

## Day 4（ch07 Planning）

### Focus
- 做出最小 Planner-Executor 双阶段流程。

### Scheduled
- [ ] 60 分钟：学习 ch07，理解 task decomposition 与 iterative planning。
- [ ] 90 分钟：实现“先产计划再执行”的 JSON plan（3-5 步即可）。
- [ ] 60 分钟：为每个计划步骤绑定可调用工具（检索/总结/核对）。
- [ ] 45 分钟：设计 4 个复杂问题，验证是否比直答更稳定。
- [ ] 45 分钟：参考 `deer-flow` 长任务编排思路，记录 3 条你能落地的机制。
- [ ] 30 分钟：写 `planning_failures.md`，记录计划失效场景。

### Someday
- [ ] 给 Planner 增加“最多迭代次数”防止无限回路。
- [ ] 对计划步骤增加优先级标签。

---

## Day 5（ch08 Multi-Agent）

### Focus
- 从单 Agent 升级到“双角色协作”最小可运行版本。

### Scheduled
- [ ] 60 分钟：学习 ch08，明确何时值得上多 Agent。
- [ ] 90 分钟：拆 2 个角色（Researcher / Verifier）并定义交接协议。
- [ ] 60 分钟：让 Verifier 仅做“证据核查 + 风险提示”。
- [ ] 45 分钟：比较单 Agent 与双 Agent 的输出质量和耗时。
- [ ] 45 分钟：参考 `crewAI` 的角色分工套路，调整你的角色描述。
- [ ] 30 分钟：形成 `multi_agent_tradeoff.md`（收益/复杂度/维护成本）。

### Someday
- [ ] 尝试加入第三角色（Coordinator）但保持可关闭。
- [ ] 为 Agent 间消息加结构化字段（intent、evidence、risk）。

---

## Day 6（ch09 Metacognition）

### Focus
- 让 Agent 能“先自检，再回答”。

### Scheduled
- [ ] 60 分钟：学习 ch09，整理自检触发条件。
- [ ] 90 分钟：实现 `self_check` 步骤（证据充分性、答案一致性、是否越权）。
- [ ] 60 分钟：把自检结果写入最终回答（简短评分 + 改进建议）。
- [ ] 45 分钟：跑 8 条问题，对比“有/无自检”差异。
- [ ] 45 分钟：参考 `AutoResearchClaw` 的自反思思路，借鉴 2 个机制。
- [ ] 30 分钟：更新 `eval_sheet.csv`。

### Someday
- [ ] 加“低分自动二次检索”机制。
- [ ] 给自检分数设人工复核阈值。

---

## Day 7（Week1 整合冲刺）

### Focus
- 产出可演示的 v0.1（单仓库、可运行、可截图）。

### Scheduled
- [ ] 90 分钟：代码整理与模块化（tools、retrieval、planning、guards 分文件）。
- [ ] 60 分钟：写一份清晰 README（启动、示例问题、已知限制）。
- [ ] 60 分钟：准备 10 条标准测试问题并跑全量。
- [ ] 45 分钟：记录指标（正确性、引用完整性、平均响应时间）。
- [ ] 45 分钟：做 1 页架构图（输入->规划->工具->自检->输出）。
- [ ] 30 分钟：录制 3-5 分钟演示脚本。
- [ ] 30 分钟：回顾本周卡点，列下周优先级。

### Someday
- [ ] 尝试把 demo 做成最小 Web UI（可选）。
- [ ] 增加 `--debug` 开关输出推理过程摘要。

---

## Day 8（ch10 Production）

### Focus
- 把“能跑”升级到“可维护、可观测”。

### Scheduled
- [ ] 60 分钟：学习 ch10，整理生产化清单（日志、重试、降级、成本）。
- [ ] 90 分钟：实现结构化日志（trace_id、step、latency、status）。
- [ ] 60 分钟：给关键工具调用加超时与重试。
- [ ] 45 分钟：增加失败兜底回复模板（明确失败原因与下一步建议）。
- [ ] 45 分钟：参考 `microsoft/agent-framework` 的 workflow 思想，优化执行链。
- [ ] 30 分钟：补 1 页 `production_readiness.md`。

### Someday
- [ ] 增加成本统计（每轮 token 估算）。
- [ ] 设计最小告警规则（错误率/超时率阈值）。

---

## Day 9（ch11 Protocols）

### Focus
- 理解并跑通“协议化工具接入”的最小案例（MCP/A2A 选一先做）。

### Scheduled
- [ ] 60 分钟：学习 ch11，区分 tool use 与 protocol 的边界。
- [ ] 90 分钟：做 1 个最小 MCP 工具接入实验（本地模拟即可）。
- [ ] 60 分钟：把协议调用结果接回你的主流程中。
- [ ] 45 分钟：写 3 条“什么时候必须上协议，什么时候没必要”。
- [ ] 45 分钟：阅读 `openai-agents-python` 或 `crewAI` 的集成示例，提炼兼容策略。
- [ ] 30 分钟：整理 `protocol_notes.md`。

### Someday
- [ ] 增加协议不可用时的降级路径。
- [ ] 对协议调用做缓存。

---

## Day 10（ch12 Context Engineering）

### Focus
- 建立稳定的上下文拼装模板，降低回答漂移。

### Scheduled
- [ ] 60 分钟：学习 ch12，拆解 prompt/history/retrieved/scratchpad 职责。
- [ ] 90 分钟：实现统一上下文构造器（可配置模板）。
- [ ] 60 分钟：为不同任务类型配置不同 prompt 模板（问答/总结/核查）。
- [ ] 45 分钟：做 6 条长对话测试，观察上下文污染问题。
- [ ] 45 分钟：参考 `dify` 或 `simstudio` 的 workflow 配置思想，改进模板化程度。
- [ ] 30 分钟：输出 `context_template.md`。

### Someday
- [ ] 加入上下文预算控制（超限时压缩历史）。
- [ ] 对 scratchpad 做脱敏。

---

## Day 11（ch13 Memory）

### Focus
- 给 Agent 增加“可控记忆”，只记该记的内容。

### Scheduled
- [ ] 60 分钟：学习 ch13，明确短期记忆 vs 长期记忆。
- [ ] 90 分钟：实现最小 memory store（本地 json/sqlite 均可）。
- [ ] 60 分钟：定义记忆写入规则（偏好、上下文、禁止项）。
- [ ] 45 分钟：设计 5 轮连续对话验证记忆效果。
- [ ] 45 分钟：参考 `deer-flow` / `OpenViking` 的记忆组织思路，提炼目录结构。
- [ ] 30 分钟：写 `memory_policy.md`。

### Someday
- [ ] 做记忆清理策略（TTL/手动删除）。
- [ ] 区分事实记忆与会话偏好记忆。

---

## Day 12（ch14 MAF 工作流）

### Focus
- 掌握 sequential / concurrent / conditional，并在项目中替换一段流程。

### Scheduled
- [ ] 60 分钟：学习 ch14 三种工作流模式。
- [ ] 90 分钟：挑一个现有流程改写为 workflow（建议 conditional）。
- [ ] 60 分钟：加入 human-in-the-loop 节点（可先模拟人工确认）。
- [ ] 45 分钟：对比改造前后吞吐与稳定性。
- [ ] 45 分钟：参考 `microsoft/agent-framework` 示例，统一你的 workflow 命名与阶段划分。
- [ ] 30 分钟：产出 `workflow_decisions.md`。

### Someday
- [ ] 增加 middleware 做统一输入输出清洗。
- [ ] 并发步骤加入资源限制策略。

---

## Day 13（ch15 Browser Use + 外部信息接入）

### Focus
- 让 Agent 能从网页抓取信息并回流到问答链路。

### Scheduled
- [ ] 60 分钟：学习 ch15 浏览器使用能力与风险边界。
- [ ] 90 分钟：实现网页抓取工具（最小化：读取页面标题/正文摘要）。
- [ ] 60 分钟：把抓取内容转为 markdown，再进入 RAG/总结链路。
- [ ] 45 分钟：做 5 条“外部网页 + 本地知识”混合问答测试。
- [ ] 45 分钟：参考 `firecrawl` 的输入规范思路，规范网页抽取输出格式。
- [ ] 30 分钟：记录合规边界（不抓私密、遵守 robots 与站点条款）。

### Someday
- [ ] 对网页内容做去噪和分段。
- [ ] 增加来源可信度标注。

---

## Day 14（Capstone + 交付）

### Focus
- 完成可展示 v0.2，并形成“下一阶段路线图”。

### Scheduled
- [ ] 90 分钟：整理代码与目录，冻结一个可运行版本。
- [ ] 60 分钟：跑最终评测集（至少 15 条问题，含对抗问题）。
- [ ] 60 分钟：输出结果报告（成功案例、失败案例、改进优先级）。
- [ ] 45 分钟：完善 README（功能、架构、运行、限制、后续计划）。
- [ ] 45 分钟：准备 5 分钟演示（问题->调用->结果->来源->失败分析）。
- [ ] 30 分钟：制定下一个两周目标（如：接 Azure Search、做 Web UI、加 CI 测试）。

### Someday
- [ ] 做简单前端面板（聊天 + 日志 + 来源展示）。
- [ ] 把评测流程脚本化，形成每次改动后的回归测试。

---

## 每日固定复盘模板（建议每天最后 30 分钟）

- 今天最有效的 1 个动作：
- 今天最卡的 1 个问题：
- 明天必须先做的 1 件事：
- 当前项目风险（高/中/低）：
- 是否达到 5 小时有效学习（是/否，原因）：

## 完成判定（两周后）

满足以下 4 条即可认为“入门达标”：

1. 能解释并实现 tool use、RAG、planning、self-check、memory 中至少 4 个能力。
2. 有 1 个可运行项目和 1 份可复现实验记录。
3. 能清楚说出单 Agent 与多 Agent 的取舍。
4. 有一份下一阶段 2-4 周的明确技术路线图。

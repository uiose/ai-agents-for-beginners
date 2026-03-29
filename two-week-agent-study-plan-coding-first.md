# Two-Week Agent Study Plan - Coding First

适用时间：`2026-03-30` 到 `2026-04-12`

目标：
- 两周内完成 `AI Agents for Beginners` 从 `ch05` 到 `ch14` 的核心学习
- 每天都要有**动手实现**，而不是只读课
- 最终做出一个可运行的 `CourseQAAgent v2`

当前进度：
- 已完成到 `ch04`

时间假设：
- `2026-03-30` 可投入 `5 小时`
- 其余每天默认投入 `2-3 小时`

执行原则：
- 每天至少完成 `1 次代码修改`
- 每天至少完成 `1 次运行验证`
- 每天至少完成 `1 条结果记录`

学习路线：
- 第一阶段：用 `lab/faq_agent_starter.py` 做小步快跑改造
- 第二阶段：用 `lab/course_qa_agent.py` 做主线项目迭代

GitHub 对照项目：
- `langgenius/dify`、`MaxKB`、`Onyx`、`DB-GPT`：参考 RAG、知识源管理、引用来源、评测
- `crewAI`、`deer-flow`：参考多 Agent / workflow 分工
- `openai/openai-agents-python`、`microsoft/agent-framework`：参考 tool calling、workflow、handoff

每天固定收尾：
- [ ] 记录今天改了哪几行代码
- [ ] 记录运行结果是否符合预期
- [ ] 记录 1 个明天继续改的点

---

## Day 1 - 2026-03-30

### Focus
- [ ] 跑通 `faq_agent_starter.py`，完成第一次真实代码修改

### Scheduled
- [ ] 运行 `lab/faq_agent_starter.py`
- [ ] 阅读 `lab/faq_LEARNING_PATH.md`
- [ ] 阅读 `lab/faq_EXERCISES.md` 的练习 1
- [ ] 修改 `TOOLS` 里的工具描述，分别测试“模糊版”和“清晰版”
- [ ] 用同一个问题做 3 次对比，记录 tool call 效果变化
- [ ] 写下你对 `schema` 的第一理解

### Someday
- [ ] 把测试问题扩成 6 个，做一版自己的 FAQ 测试集

---

## Day 2 - 2026-03-31

### Focus
- [ ] 扩展 `faq_agent_starter.py` 的数据结构，让它支持第 5 章

### Scheduled
- [ ] 完成 `lab/faq_EXERCISES.md` 的练习 2
- [ ] 在 `LESSONS_DB` 中加入第 5 章内容
- [ ] 更新 `enum: [1, 2, 3, 4]` 为包含第 5 章
- [ ] 在 `test_questions` 里补 2 个与第 5 章相关的问题
- [ ] 运行代码并验证“第 5 章讲什么”能不能答对
- [ ] 写下：为什么工具 schema 和本地数据结构必须同时更新

### Someday
- [ ] 新增一个简单工具 `list_lessons()`，让 Agent 先知道有哪些章节

---

## Day 3 - 2026-04-01

### Focus
- [ ] 给 `faq_agent_starter.py` 补上真正的工具错误处理

### Scheduled
- [ ] 完成 `lab/faq_EXERCISES.md` 的练习 3
- [ ] 先故意让工具抛异常，观察当前程序怎么失败
- [ ] 在 `run_agent()` 的工具执行部分加 `try/except`
- [ ] 让工具报错时仍返回结构化 JSON，而不是直接崩
- [ ] 重新运行并对比“修改前 vs 修改后”
- [ ] 打开 `agent_execution_log.jsonl` 看有没有记录到失败状态

### Someday
- [ ] 给日志里补一个 `error_type` 字段

---

## Day 4 - 2026-04-02

### Focus
- [ ] 给 `faq_agent_starter.py` 加权限控制，体验业务约束层

### Scheduled
- [ ] 完成 `lab/faq_EXERCISES.md` 的练习 4
- [ ] 给 `search_lesson_content()` 增加 `user_role`
- [ ] 给 `TOOLS` 参数定义加 `user_role`
- [ ] 用 `student` 身份测试访问高章节失败
- [ ] 用 `admin` 身份测试访问高章节成功
- [ ] 写下：为什么权限判断不能交给 LLM 自己决定

### Someday
- [ ] 把 `user_role` 改成从命令行参数或环境变量读取

---

## Day 5 - 2026-04-03

### Focus
- [ ] 给 `faq_agent_starter.py` 加最小会话状态，体验多轮对话

### Scheduled
- [ ] 完成 `lab/faq_EXERCISES.md` 的练习 5
- [ ] 新增 `multi_turn_conversation()` 或等价实现
- [ ] 跑一轮“第 1 章讲什么” -> “第 2 章呢？”的连续测试
- [ ] 记录现在的多轮支持到底是真的上下文记忆，还是只是脚本模拟
- [ ] 对照 `ch07 Planning` 思考状态管理和规划的区别

### Someday
- [ ] 把对话历史保存成 JSON 文件，而不是只存在内存里

---

## Day 6 - 2026-04-04

### Focus
- [ ] 给 `faq_agent_starter.py` 加强日志和调试可见性

### Scheduled
- [ ] 阅读 `lab/faq_agent_starter.py` 里的 `log_conversation()`
- [ ] 给日志增加更多字段，例如 `tool_args`、`result_preview`、`status`
- [ ] 跑完整的 `test_questions`
- [ ] 打开日志文件，检查是否足够支持你回放问题
- [ ] 把这 6 天的修改写成一页简短开发总结

### Someday
- [ ] 给 `faq_agent_starter.py` 单独写一个最小 README

---

## Day 7 - 2026-04-05

### Focus
- [ ] 切到主线项目 `course_qa_agent.py`，先扩知识范围

### Scheduled
- [ ] 运行 `course_qa_agent.py --preview`
- [ ] 运行 `course_qa_agent.py --query`
- [ ] 运行 `course_qa_agent.py --query ... --show-context`
- [ ] 修改 `DEFAULT_DOC_PATHS`，把 `ch05`、`ch06`、`ch07` 加进知识源
- [ ] 用 3 个问题重新做 preview，对比扩源前后的检索结果
- [ ] 记录：哪些问题因为扩知识源而明显改善

### Someday
- [ ] 如果效果稳定，再把 `ch08` 或你自己的笔记也加进去

---

## Day 8 - 2026-04-06

### Focus
- [ ] 像 GitHub 上的 RAG 项目那样，开始调检索效果

### Scheduled
- [ ] 阅读 `course_qa_agent.py` 里的 `extract_terms()`、`score_chunk()`、`retrieve_top_chunks()`
- [ ] 给 CLI 增加 `--top-k` 参数
- [ ] 把 `top_k` 透传到 preview 和 query 流程里
- [ ] 分别测试 `top_k=3`、`5`、`7`
- [ ] 选 5 个问题做一个最小检索对比表
- [ ] 记录：哪类问题更适合更大的 `top_k`

### Someday
- [ ] 参考 `Dify` / `Onyx` 的思路，思考后续如何加入 rerank

---

## Day 9 - 2026-04-07

### Focus
- [ ] 强化 `CourseQAAgent` 的 grounded answer 和来源约束

### Scheduled
- [ ] 阅读 `AGENT_INSTRUCTIONS`
- [ ] 修改提示词，让“资料不足时必须明确说不足”更严格
- [ ] 增强“只有实际使用资料时才输出来源”的约束
- [ ] 准备 3 个越界问题和 3 个资料不足问题
- [ ] 运行测试并观察它是否会乱答
- [ ] 记录：哪些回答方式更像 `Onyx` / `Dify` 这类知识问答产品

### Someday
- [ ] 尝试增加一个 `strict_grounding` 开关

---

## Day 10 - 2026-04-08

### Focus
- [ ] 把 `CourseQAAgent` 的“知识源管理”做得更像真实项目

### Scheduled
- [ ] 阅读 `list_available_sources()` 和 `parse_args()`
- [ ] 增加一个 `--list-sources` CLI 选项
- [ ] 让程序在不调用模型时直接列出当前知识源
- [ ] 把你自己的 1 份笔记或总结文档加入 `DEFAULT_DOC_PATHS`
- [ ] 重新跑 `--preview`，验证新知识源是否能被检索到
- [ ] 记录：加入个人笔记后，回答风格和覆盖面有什么变化

### Someday
- [ ] 把知识源拆成 `core` 和 `extended` 两组

---

## Day 11 - 2026-04-09

### Focus
- [ ] 给 `CourseQAAgent` 增加最小评测能力

### Scheduled
- [ ] 新建一个问题集文件，例如 `lab/eval_questions.json` 或 `lab/eval_questions.md`
- [ ] 至少准备 10 个问题，覆盖章节问答、概念比较、越界问题、资料不足问题
- [ ] 写一个最小批量测试入口，或新建简单脚本批量跑问题
- [ ] 保存输出结果到文件
- [ ] 人工标记哪些回答是“正确 / 部分正确 / 错误”
- [ ] 写下 3 个最值得优先修的失败模式

### Someday
- [ ] 给评测结果增加“是否给出了有效来源”这一列

---

## Day 12 - 2026-04-10

### Focus
- [ ] 吸收 workflow / handoff 思想，但先落成轻量功能而不是大重构

### Scheduled
- [ ] 学 `ch14` 的 sequential / concurrent / handoff / middleware 样例
- [ ] 对照 `openai/openai-agents-python` 和 `microsoft/agent-framework` 的思路
- [ ] 给 `course_qa_agent.py` 增加一个 `--json` 输出模式
- [ ] 在 JSON 输出里包含：answer、sources、top_chunks_preview 或 status
- [ ] 运行 3 个问题，验证它已经更像一个可集成的小服务
- [ ] 记录：当前版本更接近“脚本”还是“可集成组件”

### Someday
- [ ] 画一个 v2 设计图：retriever / answerer / evaluator 分离

---

## Day 13 - 2026-04-11

### Focus
- [ ] 收官实现 `CourseQAAgent v2`

### Scheduled
- [ ] 汇总前 6 天和后 6 天的改造点
- [ ] 把 `CourseQAAgent v2` 跑通一遍
- [ ] 确认至少具备这些能力：扩知识源、可调 top_k、可列知识源、严格来源约束、基础评测、JSON 输出
- [ ] 选 5 个代表性问题做最终演示
- [ ] 记录至少 3 个成功样例
- [ ] 记录至少 2 个失败样例和下一步修复方向

### Someday
- [ ] 参考 `crewAI` / `deer-flow`，设计一个未来的 multi-agent 版本

---

## Day 14 - 2026-04-12

### Focus
- [ ] 做最终复盘，并把这两周沉淀成可复用资产

### Scheduled
- [ ] 写一页 `README` 或 `DEVLOG`，说明你做了什么、怎么跑、现有限制是什么
- [ ] 写 1 页 cheat sheet，区分 tool use、RAG、planning、memory、multi-agent
- [ ] 对照 GitHub 参考项目写一个差距清单：
- [ ] 我现在已有的能力
- [ ] 我还缺的能力
- [ ] 下一步最值得补的 2 个方向
- [ ] 如果状态允许，把这两周的代码整理成一次 commit

### Someday
- [ ] 继续做 `15-browser-use`
- [ ] 或把 `CourseQAAgent` 升级成真正的 Web / API 服务

---

## GitHub Reference Mapping

把 GitHub 项目当“模仿点”，不要当“必须看完源码”的负担：

- `Dify / MaxKB / Onyx / DB-GPT`
- [ ] 模仿它们的 RAG、来源引用、知识源管理、评测意识

- `crewAI / deer-flow`
- [ ] 模仿它们的角色分工、流程拆解、workflow 思维

- `openai/openai-agents-python / microsoft/agent-framework`
- [ ] 模仿它们的 tool calling、workflow、handoff、可集成接口设计

---

## Completion Criteria

两周结束时，至少满足这些：

- [ ] 我修改过 `faq_agent_starter.py` 的核心逻辑，而不只是读过
- [ ] 我对 `course_qa_agent.py` 做过至少 5 处有效改造
- [ ] 我能解释检索、来源、状态、权限、错误处理分别在哪里实现
- [ ] 我有一个能跑的 `CourseQAAgent v2`
- [ ] 我能说清它和 GitHub 上典型 Agent 项目的差距在哪

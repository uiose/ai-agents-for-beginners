# GitHub 最新 Agent 应用 Top 10（第一版）

- 生成时间：2026-03-26
- 目标口径：Trending 优先（近期开星增长代理分）
- 范围：通用 Agent 应用 + RAG/知识问答 Agent
- 数据来源：GitHub Search API（多查询合并、去重后 103 个候选）

## 方法说明

本次使用了 8 条查询语句进行候选抓取，按最近活跃（pushed）先粗筛，再用代理趋势分进行排序：

趋势分（proxy）= stars / sqrt(repo_age_days) × recent_activity_boost × license_boost

- recent_activity_boost：最近 30 天有提交则加权
- license_boost：声明开源许可证则加权

说明：该趋势分是工程化近似值，不等同于 GitHub 官方 Trending 的真实开星增量。

## Top 10（平衡通用与 RAG）

| 排名 | 仓库 | 分类 | Stars | 语言 | 最近推送时间（UTC） | 趋势分（proxy） | 许可证 |
|---|---|---|---:|---|---|---:|---|
| 1 | [langgenius/dify](https://github.com/langgenius/dify) | RAG/通用平台 | 134496 | TypeScript | 2026-03-26T05:55:24Z | 4667.71 | NOASSERTION |
| 2 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | 通用 Agent | 46948 | Python | 2026-03-26T06:20:18Z | 3291.44 | MIT |
| 3 | [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | 通用 Agent | 47242 | Python | 2026-03-26T06:20:12Z | 2005.45 | MIT |
| 4 | [openai/openai-agents-python](https://github.com/openai/openai-agents-python) | 通用 Agent | 20317 | Python | 2026-03-26T06:06:41Z | 1313.22 | MIT |
| 5 | [google/adk-python](https://github.com/google/adk-python) | 通用 Agent | 18596 | Python | 2026-03-26T06:13:29Z | 1238.36 | Apache-2.0 |
| 6 | [1Panel-dev/MaxKB](https://github.com/1Panel-dev/MaxKB) | RAG/企业知识库 | 20577 | Python | 2026-03-26T04:57:55Z | 852.94 | GPL-3.0 |
| 7 | [eosphoros-ai/DB-GPT](https://github.com/eosphoros-ai/DB-GPT) | RAG/数据问答 | 18372 | Python | 2026-03-26T05:26:27Z | 705.05 | MIT |
| 8 | [Canner/WrenAI](https://github.com/Canner/WrenAI) | RAG/BI 问答 | 14689 | TypeScript | 2026-03-26T06:09:58Z | 679.00 | AGPL-3.0 |
| 9 | [onyx-dot-app/onyx](https://github.com/onyx-dot-app/onyx) | RAG/企业搜索问答 | 18031 | Python | 2026-03-26T06:20:21Z | 630.16 | NOASSERTION |
| 10 | [microsoft/agent-framework](https://github.com/microsoft/agent-framework) | 通用 Agent 框架/应用底座 | 8204 | Python | 2026-03-26T05:59:02Z | 568.18 | MIT |

## 本轮已落地的实现产物

- 原始 Top10 数据：lab/top10_agent_apps_raw.json
- Top50 评分清单：lab/top50_agent_apps_scored.csv
- 抓取脚本：lab/_collect_agent_repos.ps1

## 下一步建议

1. 将“真实 30 天开星增量”替换当前代理趋势分（通过 GraphQL stargazer 时间序列计算），结果会更接近你要求的 Trending。
2. 对 Top10 做可运行性验证（README 安装命令、最小 demo、依赖完整性），并附通过/失败原因。
3. 每周自动重跑并输出滚动榜单（保留历史对比列：上周排名、本周变动）。

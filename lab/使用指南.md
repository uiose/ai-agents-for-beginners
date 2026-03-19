# CourseQAAgent 使用指南

## 📚 项目概述

**CourseQAAgent** 是一个智能课程资料问答助手，基于 Microsoft Agent Framework 构建。它能从课程资料库中自动检索最相关的内容，然后利用 AI 模型生成准确的回答。

### 主要功能

- ✅ 自动从课程资料中检索相关内容
- ✅ 利用 AI 模型生成高质量回答
- ✅ 支持交互式对话
- ✅ 支持单个问题快速查询
- ✅ 本地检索预览（无需调用 AI）

### 适用场景

- 📖 学生快速查找课程相关概念
- 👨‍🏫 教师准备讲义和解答
- 🤖 理解 AI Agent 工作原理
- 💡 学习 Agent Framework 框架

---

## 🔧 安装和配置

### 前置条件

- **Python 版本**: 3.12 或更高
- **网络**: 需要访问 GitHub API（用于调用 AI 模型）
- **账户**: 需要有效的 GitHub 账户和 Token

### 第一步：检查 Python 环境

```bash
# 检查 Python 版本（应该是 3.12+）
python --version

# 激活虚拟环境
cd d:\agentstart\ai-agents-for-beginners
.\venv\Scripts\Activate.ps1    # Windows PowerShell
# 或
source venv/bin/activate       # Linux/Mac

# 验证依赖已安装
pip list | findstr agent-framework
```

### 第二步：配置环境变量

在 `lab` 文件夹下创建 `.env` 文件（或在项目根目录）：

```bash
# .env 文件内容
GITHUB_TOKEN=your_github_token_here
GITHUB_ENDPOINT=https://models.inference.ai.azure.com
GITHUB_MODEL_ID=gpt-4o
```

**获取 GitHub Token 的步骤**：

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 设置以下权限：
   - `repo`（完整访问私有仓库）
   - `read:user`（读取用户公开数据）
4. 生成 token 并复制保存到 `.env` 文件

### 第三步：验证配置

```bash
# 运行预览模式测试（不需要 AI 调用）
python course_qa_agent.py --preview "什么是agent"

# 输出应该显示从课程资料中检索到的内容
```

---

## 💬 三种使用方式

### 方式 1️⃣：交互式模式（默认）

最灵活的方式，可以连续提问，像聊天一样使用。

```bash
python course_qa_agent.py
```

**使用步骤**：

1. 启动程序后看到提示 `Question>`
2. 输入你的问题
3. 程序会返回 Agent 的回答
4. 继续输入新问题或输入 `exit` 退出

**示例对话**：

```
CourseQAAgent is ready. Type your question below.
Type exit to stop.

Question> 什么是 AI Agent？
=== Agent Answer ===
AI Agent 是一个能够感知环境、做出决策和采取行动的智能实体...

Question> Agent Framework 有什么特点？
=== Agent Answer ===
Agent Framework 提供了...

Question> exit
Session ended.
```

**优点**：
- 🔄 保持对话上下文
- 🎯 可以追问相关问题
- 💬 最接近真实对话体验

---

### 方式 2️⃣：单问题模式

快速获取单个问题的答案，适合集成到其他程序或脚本。

```bash
python course_qa_agent.py --query "你的问题"
```

**示例**：

```bash
# 问题1：什么是工具使用？
python course_qa_agent.py --query "什么是工具使用"

# 问题2：Agent 有哪些设计模式？
python course_qa_agent.py --query "Agent 有哪些设计模式"

# 问题3：如何使用 Azure AI Foundry？
python course_qa_agent.py --query "如何使用 Azure AI Foundry"
```

**输出格式**：

```
你的问题的直接答案...
```

**优点**：
- ⚡ 快速获取答案
- 🔗 易于自动化脚本
- 📊 便于批量处理多个问题

---

### 方式 3️⃣：预览检索模式

查看本地检索到的课程资料，**不调用 AI 模型**（节省 API 调用）。

```bash
python course_qa_agent.py --preview "你的问题"
```

**示例**：

```bash
python course_qa_agent.py --preview "什么是 Agent"
```

**输出示例**：

```
[Top 1] translations/zh-CN/01-intro-to-ai-agents/README.md | What is an AI Agent
AI Agent 是一个能够...

[Top 2] translations/zh-CN/02-explore-agentic-frameworks/README.md | Framework Overview
Agent Framework 提供了...

[Top 3] translations/zh-CN/03-agentic-design-patterns/README.md | Design Patterns
常见的 Agent 设计模式包括...
```

**用途**：
- 🔍 验证检索效果
- 💰 估计需要多少 API 调用
- 📝 手动查还是让 AI 回答
- 🐛 调试搜索相关性

---

## 📋 命令行参数详细说明

### 参数列表

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--query TEXT` | 互斥 | 无 | 提问一个问题并获得答案 |
| `--preview TEXT` | 互斥 | 无 | 预览检索到的课程资料 |
| `--show-context` | 可选 | False | 显示 AI 前面看到的背景资料 |

### 参数说明

#### 1. `--query` - 单问题模式

```bash
# 基础用法
python course_qa_agent.py --query "什么是 Design Pattern"

# 配合 --show-context 显示背景资料
python course_qa_agent.py --query "什么是 Design Pattern" --show-context
```

#### 2. `--preview` - 预览模式

```bash
# 基础用法
python course_qa_agent.py --preview "工具使用"

# 查看 Agent 在回答问题前会看到什么资料
python course_qa_agent.py --preview "Azure AI Foundry"
```

#### 3. `--show-context` - 显示检索背景

```bash
# 在交互模式中显示背景
python course_qa_agent.py --show-context

# 在单问题模式中显示背景
python course_qa_agent.py --query "Agent 工作流程" --show-context

# 输出样式：
# =========================
# === Retrieved Context Preview ===
# [Context 1]
# Source: translations/zh-CN/...
# Section: Overview
# Content: ...
# 
# [Context 2]
# ...
# =========================
```

---

## 🎯 常见使用场景

### 场景 1：快速学习某个概念

**问题**：我想快速了解什么是 "Design Pattern"

**操作**：

```bash
# 方法 A：使用预览模式快速查看资料（不消耗 API）
python course_qa_agent.py --preview "Design Pattern"

# 方法 B：让 AI 生成总结（推荐）
python course_qa_agent.py --query "什么是Design Pattern，请总结核心要点"
```

### 场景 2：准备课程讲义

**问题**：为明天的课程准备 5 个相关问题的答案

**操作**：

```bash
# 创建一个 bash 脚本 (run_qa.sh)
questions=(
    "什么是 AI Agent"
    "Agent 的应用场景有哪些"
    "如何使用 Tool Use"
    "Design Pattern 有哪些种类"
    "如何部署到生产环境"
)

for q in "${questions[@]}"; do
    echo "Q: $q"
    python course_qa_agent.py --query "$q"
    echo "---"
done
```

### 场景 3：调试搜索效果

**问题**：我的问题为什么没有找到相关资料？

**操作**：

```bash
# 1. 先看看检索到了什么
python course_qa_agent.py --preview "你的问题"

# 2. 如果没有找到，尝试改变问题表述
python course_qa_agent.py --preview "简化后的问题"

# 3. 查看 Agent 看到的具体资料
python course_qa_agent.py --query "你的问题" --show-context
```

### 场景 4：学习 Agent 框架工的作原理

**操作**：

```bash
# 1. 先预览看看架构
python course_qa_agent.py --preview "Agent Framework 架构"

# 2. 然后让 AI 解释
python course_qa_agent.py --query "Agent Framework 的架构是什么样的" --show-context

# 3. 查看源代码中的注释（文件已包含详细注释）
cat course_qa_agent.py
```

---

## ✅ 最佳实践

### ✨ 提问技巧

| 提问方式 | 效果 | 例子 |
|---------|------|------|
| **具体** | ⭐⭐⭐ | "什么是 Multi-Agent 架构" |
| **模糊** | ⭐ | "Agent 是什么" |
| **包含关键词** | ⭐⭐⭐ | "RAG Pattern 在 Agent 中的应用" |
| **多个关键词** | ⭐⭐ | "Agent Framework Design Pattern Tool" |

### 💡 效率建议

1. **使用 `--preview` 优先验证**
   - 可以节省 API 调用
   - 快速验证搜索结果

2. **交互模式最划算**
   - 一次启动，多次提问
   - 保持对话上下文
   - 节省初始化时间

3. **复杂问题分解**
   - 先问基础概念
   - 再问高级应用
   - 利用上下文记忆

### 🔒 安全建议

1. **保护你的 GitHub Token**
   ```bash
   # ❌ 错误：不要在命令行暴露 token
   export GITHUB_TOKEN=ghp_xxx
   
   # ✅ 正确：使用 .env 文件
   # .env 文件会自动被git忽略
   ```

2. **不要提交敏感信息**
   ```bash
   # .env 文件已在 .gitignore 中
   # 确保不包含其他敏感信息
   ```

---

## 🐛 故障排查

### 问题 1：环境变量缺失

**错误信息**：
```
Missing environment variables: GITHUB_TOKEN, GITHUB_ENDPOINT, GITHUB_MODEL_ID
Please update your .env file before running the agent.
```

**解决方案**：
```bash
# 1. 创建 .env 文件
cp .env.example .env    # 如果有模板的话

# 2. 编辑 .env 文件并填入值
# GITHUB_TOKEN=your_token
# GITHUB_ENDPOINT=https://models.inference.ai.azure.com
# GITHUB_MODEL_ID=gpt-4o

# 3. 验证配置
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('GITHUB_TOKEN') is not None)"
```

### 问题 2：没有相关课程资料

**症状**：
```
No relevant context found in the selected course materials.
```

**原因**：
- 问题没有在课程资料中找到匹配
- 搜索关键词不合适

**解决方案**：
```bash
# 1. 尝试使用预览模式查看
python course_qa_agent.py --preview "修改后的问题"

# 2. 列出可用资料
python course_qa_agent.py --query ""  # 空问题会列出资料源

# 3. 检查默认资料路径
# 编辑 course_qa_agent.py 的 DEFAULT_DOC_PATHS 变量
```

### 问题 3：API 连接失败

**错误信息**：
```
Agent request failed.
Reason: Connection error...
```

**解决方案**：
```bash
# 1. 检查网络连接
ping models.inference.ai.azure.com

# 2. 验证 token 有效性
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(f'Token length: {len(os.getenv(\"GITHUB_TOKEN\", \"\"))}')"

# 3. 尝试预览模式（本地操作）
python course_qa_agent.py --preview "测试"

# 4. 如果预览成功但 API 失败，说明是网络问题
```

### 问题 4：响应很慢

**原因**：
- 网络延迟
- AI 模型处理复杂问题

**优化**：
```bash
# 1. 先用预览模式测试
python course_qa_agent.py --preview "你的问题"

# 2. 简化问题
python course_qa_agent.py --query "简化后的问题"

# 3. 使用交互模式（避免重复初始化）
python course_qa_agent.py
```

---

## 📚 课程资料来源

Agent 当前可以搜索以下课程资料：

- ✅ `02-explore-agentic-frameworks/README.md` - Agent 框架探索
- ✅ `03-agentic-design-patterns/README.md` - Agent 设计模式
- ✅ `04-tool-use/README.md` - 工具使用
- ✅ `02-explore-agentic-frameworks/azure-ai-foundry-agent-creation.md` - Azure AI Foundry 指南

**扩展资料库**：

如果要添加更多课程资料，编辑 `course_qa_agent.py` 中的 `DEFAULT_DOC_PATHS` 变量：

```python
DEFAULT_DOC_PATHS = [
    # 已有的资料
    ROOT_DIR / "translations/zh-CN/02-explore-agentic-frameworks/README.md",
    # ... 其他资料 ...
    
    # 添加新资料
    ROOT_DIR / "translations/zh-CN/05-agentic-rag/README.md",
    ROOT_DIR / "translations/zh-CN/06-building-trustworthy-agents/README.md",
]
```

---

## 🔬 高级用法

### 与其他脚本集成

```python
# your_script.py
import subprocess
import json

def ask_agent(question):
    result = subprocess.run(
        ["python", "course_qa_agent.py", "--query", question],
        capture_output=True,
        text=True
    )
    return result.stdout
```

### 批量处理

```bash
# 创建 questions.txt
什么是 Agent
Agent 的应用场景
Design Pattern 有哪些
如何使用 Tool Use

# 批处理脚本
while IFS= read -r question; do
    echo "Q: $question"
    python course_qa_agent.py --query "$question" 
    echo "---"
done < questions.txt
```

### 自定义搜索权重

编辑 `score_chunk()` 函数，调整分数权重：

```python
# 完全匹配权重从 12 改为 20
if query_text and query_text in chunk.search_text:
    score += 20  # 提高完全匹配的权重
```

---

## 📖 示例命令速查

```bash
# 交互模式（推荐新手）
python course_qa_agent.py

# 快速提问
python course_qa_agent.py --query "什么是 Agent"

# 预览资料（调试用）
python course_qa_agent.py --preview "Agent"

# 显示背景资料
python course_qa_agent.py --query "Design Pattern" --show-context

# 预览 + 显示背景
python course_qa_agent.py --preview "工具使用" --show-context
```

---

## ❓ 常见问题

**Q: 我需要互联网连接吗？**
A: 需要。调用 AI 模型时需要网络。但如果只用 `--preview` 模式，可以离线使用。

**Q: API 调用有费用吗？**
A: GitHub 提供免费的 AI 模型 API。具体配额请查看 https://github.com/models

**Q: 能修改 Agent 的回答方式吗？**
A: 可以。编辑 `AGENT_INSTRUCTIONS` 变量来改变 Agent 的行为方式。

**Q: 如何添加新的课程资料？**
A: 修改 `DEFAULT_DOC_PATHS` 列表，添加新的文件路径即可。Agent 会自动加载。

**Q: 对话记录会被保存吗？**
A: 不会。每次启动程序都是新的对话。对话历史仅保存在内存中，退出后消失。

---

## 🤝 反馈和改进

遇到问题或有改进建议？

- 📝 查看代码注释（code_qa_agent.py 已包含详细中文注释）
- 🔍 查看错误信息（通常会给出明确的解决方案）
- 🐛 检查本使用指南的故障排查部分

---

**祝你使用愉快！** 🎉

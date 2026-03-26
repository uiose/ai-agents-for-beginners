# 代码修改练习：从改参数到理解逻辑

## 学习策略

```
第1步：复制运行 ✓ 代码能跑
   ↓
第2步：修改参数 → 看效果变化
   ↓
第3步：理解修改的原因
   ↓ (重复100次)
   ↓
第4步：能自己写新代码
```

---

## 练习 1：改工具描述（难度：⭐）

**目标**：体验 schema 质量对模型的影响

**当前代码**（第54行左右）：
```python
"description": "在 Agent 课程的本地内容中搜索相关知识。用于回答'第X章讲什么'或'怎样理解XXX概念'这类问题。",
```

**修改1：让描述更模糊**

改成：
```python
"description": "搜索课程",
```

然后运行代码，问同样的问题，**观察工具调用的准确率有没有下降**。

**修改2：让描述更清晰**

改成：
```python
"description": "在 1-4 号课程文件中搜索特定关键词。课程 1=基础知识，2=框架对比，3=设计模式，4=工具使用。返回包含关键词的所有句子。",
```

再运行一遍。

**问自己**：
- 三个版本中，哪个版本下 Agent 的回答最准确？
- 这为什么？
- 这跟我在 ch04_tool_review.md 里读到的"Schema 设计"有什么关系？

---

## 练习 2：添加新课程（难度：⭐⭐）

**目标**：理解工具的数据结构

**当前代码**（第27-50行）：
```python
LESSONS_DB = {
    1: {...},
    2: {...},
    3: {...},
    4: {...},
}
```

**任务**：添加第5个课程

在 `4: {...}` 后面，加上：
```python
        5: {
            "title": "生产部署",
            "content": [
                "部署选择：CLI、Web 后端、Serverless、微服务",
                "成本控制：监控 token 使用，防止滥用",
                "可靠性：错误处理、重试机制、降级策略",
            ]
        },
```

然后：
1. 更新第58行的 `enum: [1, 2, 3, 4]` 为 `enum: [1, 2, 3, 4, 5]`
2. 运行代码，问："第5章讲什么？"

**问自己**：
- 为什么 enum 也要更新？
- 如果不更新会怎样？

---

## 练习 3：让工具故意失败（难度：⭐⭐）

**目标**：体验错误处理（第3层的职责）

**当前代码**（第34行左右）：
```python
if lesson_number not in LESSONS_DB:
    return json.dumps({
        "status": "error",
        "message": f"课程 {lesson_number} 不存在（1-4 可用）"
    }, ensure_ascii=False)
```

**修改**：让某个工具调用失败

把上面的代码改成：
```python
if lesson_number not in LESSONS_DB:
    # 模拟工具故意抛异常（而不是返回 JSON）
    raise ValueError(f"课程数据库连接失败：课程 {lesson_number} 对应的数据不可用")
```

然后运行代码。

**会发生什么**：
- 你会看到 Python 错误（或者 Agent 会如何处理？）
- 这告诉你什么？

**改进**：在 `run_agent()` 函数里添加异常处理

在第145行左右的工具执行部分，改成：
```python
try:
    if tool_name == "search_lesson_content":
        tool_result = search_lesson_content(**tool_args)
    else:
        tool_result = json.dumps({"error": f"未知工具：{tool_name}"}, ensure_ascii=False)
except Exception as e:
    # 这就是第3层的错误处理
    tool_result = json.dumps({
        "status": "error",
        "message": f"工具执行失败：{str(e)}",
        "error_type": type(e).__name__
    }, ensure_ascii=False)
```

再运行一遍。**对比两次的结果**。

**问自己**：
- Agent 怎样应对工具故障的？
- 这就是为什么 ch04_tool_review.md 里说"第3层需要错误处理"

---

## 练习 4：添加权限检查（难度：⭐⭐⭐）

**目标**：体验第2层的作用（业务控制层）

现在，假设有不同权限的用户：
- `admin`：可以访问所有课程
- `student`：只能访问第1-2章

**修改方式**：

在 `search_lesson_content()` 开头，添加参数：
```python
def search_lesson_content(lesson_number: int, keyword: str, user_role: str = "student") -> str:
    """
    新增参数：user_role（用户角色）
    """
    
    # 权限检查（这就是第2层）
    if user_role == "student" and lesson_number > 2:
        return json.dumps({
            "status": "forbidden",
            "message": f"学生用户无权访问第 {lesson_number} 课程"
        }, ensure_ascii=False)
    
    # 原来的代码继续...
    LESSONS_DB = {1: {...}, ...}
    ...
```

然后在 `TOOLS` 的参数定义里添加：
```python
"user_role": {
    "type": "string",
    "enum": ["student", "admin"],
    "description": "用户角色"
}
```

再在工具调用时传入：
```python
# 大约第 145 行
if tool_name == "search_lesson_content":
    tool_result = search_lesson_content(
        **tool_args,
        user_role="student"  # ← 每次都以 student 身份调用
    )
```

运行代码，问："第3章讲什么？"

**会发生什么**：
- Agent 会尝试搜索第3章
- 工具会返回"权限不足"
- Agent 会解释为什么无法回答

**进一步**：把 `user_role="student"` 改成 `user_role="admin"`，再运行一遍。

**问自己**：
- 这就是为什么生产系统需要"第2层业务控制"
- LLM 不能决定谁能访问什么，这得由系统控制

---

## 练习 5：添加多轮对话（难度：⭐⭐⭐⭐）

**目标**：理解会话状态管理（第3层的另一个职责）

当前代码每次问题都是独立的。现在改成**记住之前的问题**。

**创建一个新函数**，在 `faq_agent_starter.py` 末尾添加：

```python
def multi_turn_conversation():
    """
    多轮对话演示。
    
    这演示了第3层需要维护会话状态。
    """
    
    # 会话状态（这应该存在数据库里，现在先存内存）
    conversation_history = []
    
    # 第一轮
    print("\n【第一轮】")
    user_input_1 = "Agent 第1章讲什么？"
    print(f"用户：{user_input_1}")
    
    # 添加到对话历史
    conversation_history.append({
        "role": "user",
        "content": user_input_1
    })
    
    result_1 = run_agent(user_input_1, verbose=False)
    print(f"Agent：{result_1['response'][:200]}...")
    
    # 保存 Agent 回复
    conversation_history.append({
        "role": "assistant",
        "content": result_1['response']
    })
    
    # 第二轮：用户提出相关问题（利用前面的对话上下文）
    print("\n【第二轮】")
    user_input_2 = "第2章呢？"  # ← 这里假设 Agent 记住了是在问课程
    print(f"用户：{user_input_2}")
    
    conversation_history.append({
        "role": "user",
        "content": user_input_2
    })
    
    result_2 = run_agent(user_input_2, verbose=False)
    print(f"Agent：{result_2['response'][:200]}...")
    
    # 完整历史
    print("\n【完整对话历史】")
    print(json.dumps(conversation_history, ensure_ascii=False, indent=2))

# 在 if __name__ == "__main__": 里调用
if __name__ == "__main__":
    # ... 原来的代码 ...
    
    # 取消注释来运行多轮对话
    # multi_turn_conversation()
```

取消注释并运行。

**问自己**：
- 没有会话历史的话，Agent 能理解"第2章呢"吗？
- 这就是为什么第3层需要"维护会话上下文"

---

## 练习总结

| 练习 | 改什么 | 学什么 | 对应的"层" |
|------|--------|--------|-----------|
| 1 | Schema 描述 | 描述质量影响模型行为 | 模型接口 |
| 2 | 添加数据 | 理解工具的数据结构 | 第4层 |
| 3 | 错误处理 | 工具失败的应对 | 第3层 |
| 4 | 权限检查 | 系统需要控制工具调用 | 第2层 |
| 5 | 会话管理 | 多轮对话需要记住历史 | 第3层 |

---

## 从修改到创新

完成这5个练习后，你会对代码的每一部分都有直观感受。

下一步就是：**能修改 → 能理解 → 能写新的**。

当你想写一个新功能（比如"添加用户反馈评分"）时，你会知道：
- 在哪里添加代码
- 数据结构怎样设计
- 要改哪几个函数

这时候，你不再是"完全不知道怎么开始"，而是"知道从哪里入手"。

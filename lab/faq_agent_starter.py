"""
最简化 Agent 项目：本地课程 FAQ 机器人
=============================================

这个项目演示了 Agent 系统的完整闭环：
1. 定义工具
2. Agent 调用工具
3. 处理工具结果
4. 返回最终答案

运行方式：
    python faq_agent_starter.py

要求：
    pip install openai python-dotenv
"""

import json
import os
from datetime import datetime
from typing import cast, Any
from dotenv import load_dotenv
from openai import OpenAI

# ============================================================================
# 第0步：加载环境变量
# ============================================================================
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ============================================================================
# 第1步：定义工具（这就是第4层的工作）
# ============================================================================

def search_lesson_content(lesson_number: int, keyword: str) -> str:
    """
    在本地课程文件中搜索内容。
    
    这是一个"虚拟工具"（实际项目中会连接真实数据库）
    """
    
    # 模拟课程内容数据库
    LESSONS_DB = {
        1: {
            "title": "Agent 基础",
            "content": [
                "Agent 是什么：智能体是能感知环境、自主决策、执行行动的系统",
                "Agent 的核心能力：观察、思考、行动的循环",
                "Function Calling：Agent 通过调用工具与外部世界交互",
            ]
        },
        2: {
            "title": "Agent 框架",
            "content": [
                "主流 Agent 框架：LangChain、AutoGen、Agent Framework",
                "框架的作用：简化 Agent 系统的开发",
                "选择框架的标准：功能完整性、学习曲线、社区活跃度",
            ]
        },
        3: {
            "title": "设计模式",
            "content": [
                "ReAct 模式：推理（Reason）+ 行动（Act）的循环",
                "思维链：让 Agent 显式地展现推理过程",
                "多智能体协作：多个 Agent 之间如何分工",
            ]
        },
        4: {
            "title": "工具使用",
            "content": [
                "工具定义：通过 schema 告诉 Agent 有哪些工具",
                "参数设计：清晰的参数说明能提高调用准确率",
                "错误处理：工具失败后 Agent 该如何应对",
            ]
        },
    }
    
    # 检查课程是否存在
    if lesson_number not in LESSONS_DB:
        return json.dumps({
            "status": "error",
            "message": f"课程 {lesson_number} 不存在（1-4 可用）"
        }, ensure_ascii=False)
    
    lesson = LESSONS_DB[lesson_number]
    
    # 搜索关键词
    results = [
        content for content in lesson["content"] 
        if keyword.lower() in content.lower()
    ]
    
    if not results:
        return json.dumps({
            "status": "not_found",
            "lesson": lesson_number,
            "lesson_title": lesson["title"],
            "message": f"课程 {lesson_number} 中未找到包含 '{keyword}' 的内容"
        }, ensure_ascii=False)
    
    return json.dumps({
        "status": "found",
        "lesson": lesson_number,
        "lesson_title": lesson["title"],
        "results": results,
        "count": len(results)
    }, ensure_ascii=False, indent=2)


# ============================================================================
# 第2步：定义工具的 schema（这是模型和系统交互的契约）
# ============================================================================

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_lesson_content",
            "description": "在 Agent 课程的本地内容中搜索相关知识。用于回答'第X章讲什么'或'怎样理解XXX概念'这类问题。",
            "parameters": {
                "type": "object",
                "properties": {
                    "lesson_number": {
                        "type": "integer",
                        "description": "课程号（1=基础，2=框架，3=设计模式，4=工具使用）",
                        "enum": [1, 2, 3, 4]
                    },
                    "keyword": {
                        "type": "string",
                        "description": "搜索关键词，例如：'推理'、'工具'、'框架'等"
                    }
                },
                "required": ["lesson_number", "keyword"]
            }
        }
    }
]

# ============================================================================
# 第3步：Agent 运行时（这就是第3层的工作）
# ============================================================================

def run_agent(user_input: str, verbose: bool = True) -> dict:
    """
    运行 Agent 的完整闭环。
    
    参数：
        user_input: 用户的问题
        verbose: 是否打印详细执行过程
    
    返回：
        包含 response（最终答案）、tools_used（使用的工具）、status（状态）的字典
    """
    
    # 1. 初始化消息历史（第3层的工作：维护会话上下文）
    messages: list = []  # type: ignore
    messages.append({
        "role": "user",
        "content": user_input
    })
    
    if verbose:
        print("\n" + "="*60)
        print(f"📝 用户输入：{user_input}")
        print("="*60)
    
    # 2. 第一次调用 LLM
    if verbose:
        print("\n🤖 [第1轮] 调用 LLM...")
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,  # type: ignore
        tools=TOOLS,  # type: ignore
        tool_choice="auto"
    )
    
    assistant_message = response.choices[0].message
    tools_used = []
    
    # 3. 检查 LLM 是否要调用工具（第3层的工作：解析输出）
    if assistant_message.tool_calls:
        if verbose:
            print(f"   → LLM 建议调用 {len(assistant_message.tool_calls)} 个工具")
        
        # 添加 LLM 的回复到消息历史
        if assistant_message.tool_calls:
            tool_calls_list = []
            for tc in assistant_message.tool_calls:
                tool_calls_list.append({
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,  # type: ignore
                        "arguments": tc.function.arguments  # type: ignore
                    }
                })
            
            messages.append({  # type: ignore
                "role": "assistant",
                "content": assistant_message.content or "",
                "tool_calls": tool_calls_list
            })
        
        # 4. 依次执行工具（第4层的工作：执行）
        for tool_call in assistant_message.tool_calls:
            tool_name = tool_call.function.name  # type: ignore
            tool_args = json.loads(tool_call.function.arguments)  # type: ignore
            
            if verbose:
                print(f"\n🔧 执行工具：{tool_name}")
                print(f"   参数：{tool_args}")
            
            # 执行对应的工具函数
            if tool_name == "search_lesson_content":
                tool_result = search_lesson_content(**tool_args)
            else:
                tool_result = json.dumps({"error": f"未知工具：{tool_name}"}, ensure_ascii=False)
            
            if verbose:
                print(f"   结果：{tool_result[:100]}...")  # 只打印前100个字符
            
            tools_used.append({
                "name": tool_name,
                "args": tool_args,
                "result_preview": tool_result[:100]
            })
            
            # 5. 将工具结果注入回消息历史（第3层的工作：回传结果）
            messages.append({  # type: ignore
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })
        
        # 6. 第二次调用 LLM，让它基于工具结果生成最终答案
        if verbose:
            print("\n🤖 [第2轮] 根据工具结果调用 LLM 生成答案...")
        
        final_response = client.chat.completions.create(
            model="gpt-4",
            messages=messages  # type: ignore
        )
        
        final_answer = final_response.choices[0].message.content
        status = "success_with_tools"
    
    else:
        # LLM 直接回答，不需要工具
        if verbose:
            print("   → LLM 直接回答，不需要调用工具")
        
        final_answer = assistant_message.content
        status = "success_no_tools"
    
    # 7. 返回结果（这是 Agent Runtime 的输出）
    return {
        "response": final_answer,
        "tools_used": tools_used,
        "status": status,
        "timestamp": datetime.now().isoformat()
    }

# ============================================================================
# 第4步：日志记录（这是第5层的工作）
# ============================================================================

def log_conversation(user_input: str, result: dict):
    """记录对话到文件，用于后期分析和调试"""
    
    log_file = "agent_execution_log.jsonl"
    
    log_entry = {
        "timestamp": result["timestamp"],
        "user_input": user_input,
        "response_preview": result["response"][:100] + "..." if len(result["response"]) > 100 else result["response"],
        "tools_used": [tool["name"] for tool in result["tools_used"]],
        "status": result["status"]
    }
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

# ============================================================================
# 第5步：主程序（演示如何使用）
# ============================================================================

if __name__ == "__main__":
    
    # 示例问题列表
    test_questions = [
        "Agent 第1章讲什么？",
        "怎样理解推理过程？",
        "有哪些主流框架？",
        "工具失败了怎么办？",
    ]
    
    print("\n" + "="*60)
    print("🚀 本地课程 FAQ 机器人 - 启动")
    print("="*60)
    
    for question in test_questions:
        # 运行 Agent
        result = run_agent(question, verbose=True)
        
        # 记录结果
        log_conversation(question, result)
        
        # 打印最终答案
        print("\n📤 最终答案：")
        print("-" * 60)
        print(result["response"])
        print("-" * 60)
        
        input("\n按 Enter 继续下一个问题...")
    
    print("\n✅ 演示完成！")
    print(f"📊 执行日志已保存到 agent_execution_log.jsonl")

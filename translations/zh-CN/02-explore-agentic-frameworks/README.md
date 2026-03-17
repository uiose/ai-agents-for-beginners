[![探索 AI 代理框架](../../../translated_images/zh-CN/lesson-2-thumbnail.c65f44c93b8558df.webp)](https://youtu.be/ODwF-EZo_O8?si=1xoy_B9RNQfrYdF7)

> _(点击上方图片观看本课视频)_

# 探索 AI 代理框架

AI 代理框架是为简化 AI 代理的创建、部署和管理而设计的软件平台。这些框架为开发人员提供预构建的组件、抽象和工具，从而简化复杂 AI 系统的开发。

这些框架通过为 AI 代理开发中常见的挑战提供标准化方法，帮助开发人员专注于其应用的独特方面。它们增强了构建 AI 系统时的可扩展性、可访问性和效率。

## 介绍 

本课将覆盖：

- 什么是 AI 代理框架，它们使开发人员能够实现什么？
- 团队如何使用这些框架快速原型、迭代并改进其代理的能力？
- 由 Microsoft <a href="https://aka.ms/ai-agents/autogen" target="_blank">AutoGen</a>、<a href="https://aka.ms/ai-agents-beginners/semantic-kernel" target="_blank">Semantic Kernel</a> 和 <a href="https://aka.ms/ai-agents-beginners/ai-agent-service" target="_blank">Azure AI Agent Service</a> 创建的框架和工具之间有什么区别？
- 我可以直接集成现有的 Azure 生态系统工具，还是需要独立的解决方案？
- 什么是 Azure AI Agents 服务，它如何帮助我？

## 学习目标

本课的目标是帮助你理解：

- AI 代理框架在 AI 开发中的作用。
- 如何利用 AI 代理框架构建智能代理。
- AI 代理框架启用的关键能力。
- AutoGen、Semantic Kernel 和 Azure AI Agent Service 之间的差异。

## 什么是 AI 代理框架，它们使开发人员能够做什么？

传统的 AI 框架可以帮助你将 AI 集成到应用中，并以以下方式提升这些应用：

- **个性化**：AI 可以分析用户行为和偏好，提供个性化的推荐、内容和体验。
Example: 流媒体服务如 Netflix 使用 AI 根据观看历史推荐电影和节目，从而提升用户参与度和满意度。
- **自动化与效率**：AI 可以自动执行重复性任务，简化工作流程，提高运营效率。
Example: 客服应用使用 AI 驱动的聊天机器人处理常见询问，缩短响应时间并让人工客服可以处理更复杂的问题。
- **增强用户体验**：AI 可以通过语音识别、自然语言处理和预测文本等智能功能改善整体用户体验。
Example: 虚拟助手如 Siri 和 Google Assistant 使用 AI 理解并响应语音指令，使用户更容易与设备交互。

### 这听起来都很棒，那么为什么我们还需要 AI 代理框架？

AI 代理框架不仅仅是普通的 AI 框架。它们旨在支持创建能够与用户、其他代理和环境交互以实现特定目标的智能代理。这些代理可以表现出自主行为、做出决策并适应变化条件。让我们看看 AI 代理框架启用的一些关键能力：

- **代理协作与协调**：支持创建多个可以协同工作、沟通并协调以解决复杂任务的 AI 代理。
- **任务自动化与管理**：提供用于自动化多步骤工作流、任务委派和代理间动态任务管理的机制。
- **上下文理解与适应**：赋予代理理解上下文、适应变化环境并基于实时信息做决策的能力。

总之，代理让你能够做更多事情，将自动化提升到一个新的水平，创建能够从环境中适应和学习的更智能系统。

## 如何快速原型、迭代并改进代理的能力？

这是一个快速发展的领域，但在大多数 AI 代理框架中，有一些共同点可以帮助你快速原型和迭代，即模块化组件、协作工具和实时学习。让我们深入了解这些内容：

- **使用模块化组件**：AI SDK 提供预构建组件，例如 AI 和记忆连接器、使用自然语言或代码插件的函数调用、提示模板等。
- **利用协作工具**：为代理设计特定角色和任务，使其能够测试和完善协作工作流。
- **实时学习**：实现反馈回路，使代理从交互中学习并动态调整其行为。

### 使用模块化组件

像 Microsoft Semantic Kernel 和 LangChain 这样的 SDK 提供预构建组件，例如 AI 连接器、提示模板和记忆管理。

**团队如何使用这些**：团队可以快速组合这些组件来创建功能原型，而无需从头开始，从而实现快速试验和迭代。

**实践中的工作方式**：你可以使用预构建的解析器从用户输入中提取信息，使用记忆模块存储和检索数据，并使用提示生成器与用户交互，所有这些都不需要你从零构建这些组件。

**示例代码**. 下面让我们看看如何使用 Semantic Kernel Python 和 .Net 的预构建 AI 连接器，通过自动函数调用让模型响应用户输入的示例：

``` python
# 语义内核 Python 示例

import asyncio
from typing import Annotated

from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import kernel_function
from semantic_kernel.kernel import Kernel

# 定义一个 ChatHistory 对象以保存对话上下文
chat_history = ChatHistory()
chat_history.add_user_message("I'd like to go to New York on January 1, 2025")


# 定义一个包含预订旅行功能的示例插件
class BookTravelPlugin:
    """A Sample Book Travel Plugin"""

    @kernel_function(name="book_flight", description="Book travel given location and date")
    async def book_flight(
        self, date: Annotated[str, "The date of travel"], location: Annotated[str, "The location to travel to"]
    ) -> str:
        return f"Travel was booked to {location} on {date}"

# 创建内核
kernel = Kernel()

# 将示例插件添加到内核对象中
kernel.add_plugin(BookTravelPlugin(), plugin_name="book_travel")

# 定义 Azure OpenAI AI 连接器
chat_service = AzureChatCompletion(
    deployment_name="YOUR_DEPLOYMENT_NAME", 
    api_key="YOUR_API_KEY", 
    endpoint="https://<your-resource>.azure.openai.com/",
)

# 定义请求设置以配置具有自动函数调用的模型
request_settings = AzureChatPromptExecutionSettings(function_choice_behavior=FunctionChoiceBehavior.Auto())


async def main():
    # 根据给定的聊天记录和请求设置向模型发出请求
    # 内核包含模型将请求调用的示例
    response = await chat_service.get_chat_message_content(
        chat_history=chat_history, settings=request_settings, kernel=kernel
    )
    assert response is not None

    """
    Note: In the auto function calling process, the model determines it can invoke the 
    `BookTravelPlugin` using the `book_flight` function, supplying the necessary arguments. 
    
    For example:

    "tool_calls": [
        {
            "id": "call_abc123",
            "type": "function",
            "function": {
                "name": "BookTravelPlugin-book_flight",
                "arguments": "{'location': 'New York', 'date': '2025-01-01'}"
            }
        }
    ]

    Since the location and date arguments are required (as defined by the kernel function), if the 
    model lacks either, it will prompt the user to provide them. For instance:

    User: Book me a flight to New York.
    Model: Sure, I'd love to help you book a flight. Could you please specify the date?
    User: I want to travel on January 1, 2025.
    Model: Your flight to New York on January 1, 2025, has been successfully booked. Safe travels!
    """

    print(f"`{response}`")
    # 示例 AI 模型响应：`您预订的2025年1月1日飞往纽约的航班已成功订票。祝您旅途愉快！✈️🗽`

    # 将模型的响应添加到我们的聊天历史上下文中
    chat_history.add_assistant_message(response.content)


if __name__ == "__main__":
    asyncio.run(main())
```
```csharp
// Semantic Kernel C# example

using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using System.ComponentModel;
using Microsoft.SemanticKernel.Connectors.AzureOpenAI;

ChatHistory chatHistory = [];
chatHistory.AddUserMessage("I'd like to go to New York on January 1, 2025");

var kernelBuilder = Kernel.CreateBuilder();
kernelBuilder.AddAzureOpenAIChatCompletion(
    deploymentName: "NAME_OF_YOUR_DEPLOYMENT",
    apiKey: "YOUR_API_KEY",
    endpoint: "YOUR_AZURE_ENDPOINT"
);
kernelBuilder.Plugins.AddFromType<BookTravelPlugin>("BookTravel"); 
var kernel = kernelBuilder.Build();

var settings = new AzureOpenAIPromptExecutionSettings()
{
    FunctionChoiceBehavior = FunctionChoiceBehavior.Auto()
};

var chatCompletion = kernel.GetRequiredService<IChatCompletionService>();

var response = await chatCompletion.GetChatMessageContentAsync(chatHistory, settings, kernel);

/*
Behind the scenes, the model recognizes the tool to call, what arguments it already has (location) and (date)
{

"tool_calls": [
    {
        "id": "call_abc123",
        "type": "function",
        "function": {
            "name": "BookTravelPlugin-book_flight",
            "arguments": "{'location': 'New York', 'date': '2025-01-01'}"
        }
    }
]
*/

Console.WriteLine(response.Content);
chatHistory.AddMessage(response!.Role, response!.Content!);

// Example AI Model Response: Your flight to New York on January 1, 2025, has been successfully booked. Safe travels! ✈️🗽

// Define a plugin that contains the function to book travel
public class BookTravelPlugin
{
    [KernelFunction("book_flight")]
    [Description("Book travel given location and date")]
    public async Task<string> BookFlight(DateTime date, string location)
    {
        return await Task.FromResult( $"Travel was booked to {location} on {date}");
    }
}
```

从此示例中你可以看到如何利用预构建的解析器从用户输入中提取关键信息，例如航班预订请求的出发地、目的地和日期。这种模块化方法让你可以专注于高层逻辑。

### 利用协作工具

像 CrewAI、Microsoft AutoGen 和 Semantic Kernel 这样的框架便于创建可以协同工作的多个代理。

**团队如何使用这些**：团队可以为代理设计特定的角色和任务，使其能够测试和完善协作工作流并提高整体系统效率。

**实践中的工作方式**：你可以创建一个代理团队，每个代理具有专门功能，例如数据检索、分析或决策。这些代理可以相互沟通并共享信息以实现共同目标，例如回答用户查询或完成任务。

**示例代码 (AutoGen)**：

```python
# 创建代理，然后创建一个循环调度，让他们可以一起工作，这种情况下是按顺序进行

# 数据检索代理
# 数据分析代理
# 决策代理

agent_retrieve = AssistantAgent(
    name="dataretrieval",
    model_client=model_client,
    tools=[retrieve_tool],  # 该代理只负责调用检索工具拿数据
    system_message="Use tools to solve tasks."
)

agent_analyze = AssistantAgent(
    name="dataanalysis",
    model_client=model_client,
    tools=[analyze_tool],  # 该代理只负责调用分析工具处理数据
    system_message="Use tools to solve tasks."
)

# 当用户说“APPROVE”时对话结束
termination = TextMentionTermination("APPROVE")

# 用户代理：需要人工确认或补充信息时，会通过 input_func=input 向终端读取输入
user_proxy = UserProxyAgent("user_proxy", input_func=input)

# 轮询群聊：按顺序让各代理发言（检索 -> 分析 -> 用户），并使用 termination 作为终止条件
team = RoundRobinGroupChat([agent_retrieve, agent_analyze, user_proxy], termination_condition=termination)

# 以流式方式运行任务，最多 10 轮对话
stream = team.run_stream(task="Analyze data", max_turns=10)
# 将流式结果实时输出到控制台；在脚本中运行时通常放在 asyncio.run(...) 的异步上下文中
await Console(stream)
```

在上面的代码中，你可以看到如何创建一个涉及多个代理协作分析数据的任务。每个代理执行特定功能，通过协调代理来执行任务以达到期望结果。通过创建具有专门角色的专用代理，可以提高任务效率和性能。

### 实时学习

先进的框架提供实时上下文理解和自适应的能力。

**团队如何使用这些**：团队可以实现反馈回路，让代理从交互中学习并动态调整其行为，从而持续改进和完善能力。

**实践中的工作方式**：代理可以分析用户反馈、环境数据和任务结果来更新其知识库、调整决策算法，并随着时间提升性能。这种迭代学习过程使代理能够适应变化的条件和用户偏好，增强整体系统效果。

## AutoGen、Semantic Kernel 和 Azure AI Agent Service 之间有什么不同？

有许多比较这些框架的方法，但让我们从它们的设计、能力和目标用例的一些关键差异来看看：

## AutoGen

AutoGen 是由微软研究院的 AI 前沿实验室开发的开源框架。它专注于事件驱动的、分布式的 *agentic* 应用，支持多模型（LLM 和 SLM）、工具和高级多代理设计模式。

AutoGen 围绕代理的核心概念构建，代理是能够感知环境、做出决策并采取行动以实现特定目标的自治实体。代理通过异步消息进行通信，使它们能够独立并行工作，从而增强系统的可扩展性和响应性。

<a href="https://en.wikipedia.org/wiki/Actor_model" target="_blank">代理基于 Actor 模型</a>。根据维基百科，actor 是 _并发计算的基本构建块。作为对其接收的消息的响应，actor 可以：做出本地决策、创建更多 actor、发送更多消息，并决定如何响应接下来收到的消息_。

**用例**：自动化代码生成、数据分析任务，以及为规划和研究功能构建定制代理。

以下是 AutoGen 的一些重要核心概念：

- **代理**。代理是一个软件实体：
  - **通过消息进行通信**，这些消息可以是同步或异步的。
  - **维护自己的状态**，该状态可以被传入的消息修改。
  - **执行动作**以响应接收到的消息或其状态的变化。这些动作可能修改代理的状态并产生外部效果，例如更新消息日志、发送新消息、执行代码或进行 API 调用。
    
  这里有一个简短的代码片段，你可以在其中创建具有聊天能力的自定义代理：

    ```python
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.messages import TextMessage
    from autogen_ext.models.openai import OpenAIChatCompletionClient


    class MyAgent(RoutedAgent):
        def __init__(self, name: str) -> None:
            super().__init__(name)
            model_client = OpenAIChatCompletionClient(model="gpt-4o")
            self._delegate = AssistantAgent(name, model_client=model_client)
    
        @message_handler
        async def handle_my_message_type(self, message: MyMessageType, ctx: MessageContext) -> None:
            print(f"{self.id.type} received message: {message.content}")
            response = await self._delegate.on_messages(
                [TextMessage(content=message.content, source="user")], ctx.cancellation_token
            )
            print(f"{self.id.type} responded: {response.chat_message.content}")
    ```
    
    在上面的代码中，`MyAgent` 已被创建并继承自 `RoutedAgent`。它有一个消息处理器，用于打印消息内容，然后使用 `AssistantAgent` 委托发送响应。特别注意我们如何将 `self._delegate` 赋值为 `AssistantAgent` 的一个实例，`AssistantAgent` 是一个可处理聊天完成的预构建代理。


    下面让 AutoGen 知道这种代理类型并启动程序：

    ```python
    
    # main.py
    runtime = SingleThreadedAgentRuntime()
    await MyAgent.register(runtime, "my_agent", lambda: MyAgent())

    runtime.start()  # 在后台开始处理消息。
    await runtime.send_message(MyMessageType("Hello, World!"), AgentId("my_agent", "default"))
    ```

    在上面的代码中，代理已在运行时注册，然后向代理发送了一条消息，产生了如下输出：

    ```text
    # Output from the console:
    my_agent received message: Hello, World!
    my_assistant received message: Hello, World!
    my_assistant responded: Hello! How can I assist you today?
    ```

- **多代理**。AutoGen 支持创建可以协同工作以完成复杂任务的多个代理。代理可以通信、共享信息并协调它们的行动以更高效地解决问题。要创建多代理系统，你可以定义具有专门功能和角色的不同类型代理，例如数据检索、分析、决策和用户交互。下面我们看看这样的创建是如何呈现的，以便更好地理解：

    ```python
    editor_description = "Editor for planning and reviewing the content."

    # 声明代理的示例
    editor_agent_type = await EditorAgent.register(
    runtime,
    editor_topic_type,  # 使用主题类型作为代理类型。
    lambda: EditorAgent(
        description=editor_description,
        group_chat_topic_type=group_chat_topic_type,
        model_client=OpenAIChatCompletionClient(
            model="gpt-4o-2024-08-06",
            # api_key="你的_API_密钥",
        ),
        ),
    )

    # 其余声明为简洁而省略

    # 群聊
    group_chat_manager_type = await GroupChatManager.register(
    runtime,
    "group_chat_manager",
    lambda: GroupChatManager(
        participant_topic_types=[writer_topic_type, illustrator_topic_type, editor_topic_type, user_topic_type],
        model_client=OpenAIChatCompletionClient(
            model="gpt-4o-2024-08-06",
            # api_key="你的_API_密钥",
        ),
        participant_descriptions=[
            writer_description, 
            illustrator_description, 
            editor_description, 
            user_description
        ],
        ),
    )
    ```

    在上面的代码中，我们有一个已在运行时注册的 `GroupChatManager`。该管理器负责协调不同类型代理之间的交互，例如撰稿人、插画师、编辑和用户。

- **代理运行时**。该框架提供运行时环境，支持代理之间的通信、管理它们的身份和生命周期，并强制执行安全和隐私边界。这意味着你可以在安全且受控的环境中运行代理，确保它们能够安全且高效地交互。有两个值得关注的运行时：
  - **独立运行时**。对于所有代理在同一编程语言中实现并运行在同一进程中的单进程应用，这是一个不错的选择。下面是其工作方式的示意图：
  
    <a href="https://microsoft.github.io/autogen/stable/_images/architecture-standalone.svg" target="_blank">独立运行时</a>   
应用堆栈

    *代理通过运行时以消息方式通信，运行时管理代理的生命周期*

  - **分布式代理运行时**，适用于代理可能在不同编程语言中实现并部署在不同机器上的多进程应用。下面是其工作方式的示意图：
  
    <a href="https://microsoft.github.io/autogen/stable/_images/architecture-distributed.svg" target="_blank">分布式运行时</a>

## Semantic Kernel + 代理框架

Semantic Kernel 是面向企业的 AI 协同编排 SDK。它由 AI 和记忆连接器以及一个代理框架组成。

我们先介绍一些核心组件：

- **AI 连接器**：这是一个用于在 Python 和 C# 中与外部 AI 服务和数据源接口的组件。

  ```python
  # 语义内核 Python
  from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
  from semantic_kernel.kernel import Kernel

  kernel = Kernel()
  kernel.add_service(
    AzureChatCompletion(
        deployment_name="your-deployment-name",
        api_key="your-api-key",
        endpoint="your-endpoint",
    )
  )
  ```  

    ```csharp
    // Semantic Kernel C#
    using Microsoft.SemanticKernel;

    // Create kernel
    var builder = Kernel.CreateBuilder();
    
    // Add a chat completion service:
    builder.Services.AddAzureOpenAIChatCompletion(
        "your-resource-name",
        "your-endpoint",
        "your-resource-key",
        "deployment-model");
    var kernel = builder.Build();
    ```

    这里有一个简单示例，展示如何创建一个 kernel 并添加聊天完成服务。Semantic Kernel 会与外部 AI 服务建立连接，在此示例中为 Azure OpenAI 聊天完成服务。

- **插件**：这些封装了应用可以使用的函数。既有现成插件，也有你可以创建的自定义插件。一个相关概念是“提示函数”。你不是为函数调用提供自然语言提示，而是向模型广播某些函数。基于当前聊天上下文，模型可能选择调用这些函数中的一个来完成请求或查询。示例如下：

  ```python
  from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatCompletion


  async def main():
      from semantic_kernel.functions import KernelFunctionFromPrompt
      from semantic_kernel.kernel import Kernel

      kernel = Kernel()
      kernel.add_service(AzureChatCompletion())

      user_input = input("User Input:> ")

      kernel_function = KernelFunctionFromPrompt(
          function_name="SummarizeText",
          prompt="""
          Summarize the provided unstructured text in a sentence that is easy to understand.
          Text to summarize: {{$user_input}}
          """,
      )

      response = await kernel_function.invoke(kernel=kernel, user_input=user_input)
      print(f"Model Response: {response}")

      """
      Sample Console Output:

      User Input:> I like dogs
      Model Response: The text expresses a preference for dogs.
      """


  if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
  ```

    ```csharp
    var userInput = Console.ReadLine();

    // Define semantic function inline.
    string skPrompt = @"Summarize the provided unstructured text in a sentence that is easy to understand.
                        Text to summarize: {{$userInput}}";
    
    // create the function from the prompt
    KernelFunction summarizeFunc = kernel.CreateFunctionFromPrompt(
        promptTemplate: skPrompt,
        functionName: "SummarizeText"
    );

    //then import into the current kernel
    kernel.ImportPluginFromFunctions("SemanticFunctions", [summarizeFunc]);

    ```

    在这里，你首先有一个模板提示 `skPrompt`，它为用户输入文本 `$userInput` 留出空间。然后你创建了 kernel 函数 `SummarizeText`，并以插件名 `SemanticFunctions` 将其导入到 kernel 中。注意函数的名称，这有助于 Semantic Kernel 理解该函数的用途以及何时应调用它。

- **本地函数**：框架也可以直接调用本地函数来执行任务。下面是一个从文件检索内容的本地函数示例：

    ```csharp
    public class NativeFunctions {

        [SKFunction, Description("Retrieve content from local file")]
        public async Task<string> RetrieveLocalFile(string fileName, int maxSize = 5000)
        {
            string content = await File.ReadAllTextAsync(fileName);
            if (content.Length <= maxSize) return content;
            return content.Substring(0, maxSize);
        }
    }
    
    //Import native function
    string plugInName = "NativeFunction";
    string functionName = "RetrieveLocalFile";

   //To add the functions to a kernel use the following function
    kernel.ImportPluginFromType<NativeFunctions>();

    ```

- **记忆**：抽象并简化了 AI 应用的上下文管理。记忆的理念是这些信息是 LLM 应该知道的内容。你可以将这些信息存储在向量存储中，该存储最终可能是内存数据库、向量数据库或类似结构。下面是一个非常简化的场景示例，其中 *facts* 被添加到记忆中：

    ```csharp
    var facts = new Dictionary<string,string>();
    facts.Add(
        "Azure Machine Learning; https://learn.microsoft.com/azure/machine-learning/",
        @"Azure Machine Learning is a cloud service for accelerating and
        managing the machine learning project lifecycle. Machine learning professionals,
        data scientists, and engineers can use it in their day-to-day workflows"
    );
    
    facts.Add(
        "Azure SQL Service; https://learn.microsoft.com/azure/azure-sql/",
        @"Azure SQL is a family of managed, secure, and intelligent products
        that use the SQL Server database engine in the Azure cloud."
    );
    
    string memoryCollectionName = "SummarizedAzureDocs";
    
    foreach (var fact in facts) {
        await memoryBuilder.SaveReferenceAsync(
            collection: memoryCollectionName,
            description: fact.Key.Split(";")[1].Trim(),
            text: fact.Value,
            externalId: fact.Key.Split(";")[2].Trim(),
            externalSourceName: "Azure Documentation"
        );
    }
    ```

    这些事实随后被存储在内存集合 `SummarizedAzureDocs` 中。这是一个非常简化的示例，但您可以看到如何将信息存储在内存中以供 LLM 使用。

So that's the basics of the Semantic Kernel framework, what about the Agent Framework?

## Azure AI Agent 服务

Azure AI Agent 服务是最近新增的服务，于 Microsoft Ignite 2024 上发布。它允许使用更灵活的模型开发和部署 AI 代理，例如直接调用像 Llama 3、Mistral 和 Cohere 这样的开源 LLM。

Azure AI Agent 服务提供更强的企业级安全机制和数据存储方法，适用于企业应用。 

它开箱即用地支持像 AutoGen 和 Semantic Kernel 这样的多代理编排框架。

该服务目前处于公开预览阶段，支持使用 Python 和 C# 构建代理。

Using Semantic Kernel Python, we can create an Azure AI Agent with a user-defined plugin:

```python
import asyncio
from typing import Annotated

from azure.identity.aio import DefaultAzureCredential

from semantic_kernel.agents import AzureAIAgent, AzureAIAgentSettings, AzureAIAgentThread
from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.contents import AuthorRole
from semantic_kernel.functions import kernel_function


# 定义一个示例插件用于示例
class MenuPlugin:
    """A sample Menu Plugin used for the concept sample."""

    @kernel_function(description="Provides a list of specials from the menu.")
    def get_specials(self) -> Annotated[str, "Returns the specials from the menu."]:
        return """
        Special Soup: Clam Chowder
        Special Salad: Cobb Salad
        Special Drink: Chai Tea
        """

    @kernel_function(description="Provides the price of the requested menu item.")
    def get_item_price(
        self, menu_item: Annotated[str, "The name of the menu item."]
    ) -> Annotated[str, "Returns the price of the menu item."]:
        return "$9.99"


async def main() -> None:
    ai_agent_settings = AzureAIAgentSettings.create()

    async with (
        DefaultAzureCredential() as creds,
        AzureAIAgent.create_client(
            credential=creds,
            conn_str=ai_agent_settings.project_connection_string.get_secret_value(),
        ) as client,
    ):
        # 创建代理定义
        agent_definition = await client.agents.create_agent(
            model=ai_agent_settings.model_deployment_name,
            name="Host",
            instructions="Answer questions about the menu.",
        )

        # 使用已定义的客户端和代理定义创建 AzureAI 代理
        agent = AzureAIAgent(
            client=client,
            definition=agent_definition,
            plugins=[MenuPlugin()],
        )

        # 创建一个线程来保存对话
        # 如果未提供线程，将创建一个新线程
        # 并将其与初始响应一起返回
        thread: AzureAIAgentThread | None = None

        user_inputs = [
            "Hello",
            "What is the special soup?",
            "How much does that cost?",
            "Thank you",
        ]

        try:
            for user_input in user_inputs:
                print(f"# User: '{user_input}'")
                # 调用指定线程的代理
                response = await agent.get_response(
                    messages=user_input,
                    thread_id=thread,
                )
                print(f"# {response.name}: {response.content}")
                thread = response.thread
        finally:
            await thread.delete() if thread else None
            await client.agents.delete_agent(agent.id)


if __name__ == "__main__":
    asyncio.run(main())
```

### 核心概念

Azure AI Agent 服务具有以下核心概念：

- **Agent**. Azure AI Agent 服务与 Microsoft Foundry 集成。在 AI Foundry 内，AI Agent 充当一个“智能”微服务，可用于回答问题（RAG）、执行操作或完全自动化工作流。它通过将生成式 AI 模型的能力与允许其访问和交互真实世界数据源的工具相结合来实现这一点。下面是一个代理示例：

    ```python
    agent = project_client.agents.create_agent(
        model="gpt-4o-mini",
        name="my-agent",
        instructions="You are helpful agent",
        tools=code_interpreter.definitions,
        tool_resources=code_interpreter.resources,
    )
    ```

    在此示例中，使用模型 `gpt-4o-mini` 创建了一个代理，名称为 `my-agent`，指令为 `You are helpful agent`。该代理配备了执行代码解释任务的工具和资源。

- **Thread and messages**. 线程是另一个重要概念。它表示代理与用户之间的对话或交互。线程可用于跟踪对话进度、存储上下文信息并管理交互的状态。下面是一个线程示例：

    ```python
    thread = project_client.agents.create_thread()
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Could you please create a bar chart for the operating profit using the following data and provide the file to me? Company A: $1.2 million, Company B: $2.5 million, Company C: $3.0 million, Company D: $1.8 million",
    )
    
    # Ask the agent to perform work on the thread
    run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
    
    # Fetch and log all messages to see the agent's response
    messages = project_client.agents.list_messages(thread_id=thread.id)
    print(f"Messages: {messages}")
    ```

    在前面的代码中，创建了一个线程。之后向该线程发送了一条消息。通过调用 `create_and_process_run`，请求代理在该线程上执行工作。最后，获取并记录消息以查看代理的响应。这些消息表明了用户与代理之间对话的进展。还需要理解的是，消息可以是不同类型，例如文本、图像或文件，也就是说，代理的工作可能产生例如图像或文本响应。作为开发者，您可以使用这些信息进一步处理响应或将其呈现给用户。

- **Integrates with other AI frameworks**. Azure AI Agent 服务可以与 AutoGen 和 Semantic Kernel 等其他框架交互，这意味着您可以在这些框架之一中构建应用的一部分，例如使用 Agent 服务作为编排器，或者您也可以在 Agent 服务中构建全部内容。

**用例**: Azure AI Agent 服务旨在为需要安全、可扩展且灵活的 AI 代理部署的企业应用而设计。

## 这些框架之间有什么区别？
 
听起来这些框架确实有很多重叠，但在设计、功能和目标用例方面存在一些关键差异：
 
- **AutoGen**: 是一个专注于多代理系统前沿研究的试验框架。它是实验和原型设计复杂多代理系统的最佳场所。
- **Semantic Kernel**: 是一个为构建企业代理应用而准备的生产就绪代理库。专注于事件驱动、分布式的代理应用，支持多个 LLM 和 SLM、工具以及单/多代理设计模式。
- **Azure AI Agent Service**: 是 Azure Foundry 中用于代理的平台和部署服务。它提供与 Azure Foundry 支持的服务（如 Azure OpenAI、Azure AI Search、Bing Search 和代码执行）的连接构建。
 
Still not sure which one to choose?

### 使用场景
 
让我们通过一些常见用例来帮助您：
 
> Q: I'm experimenting, learning and building proof-of-concept agent applications, and I want to be able to build and experiment quickly
>
>
>A: AutoGen 对于此场景是一个不错的选择，因为它专注于事件驱动、分布式的代理应用，并支持高级的多代理设计模式。

> Q: What makes AutoGen a better choice than Semantic Kernel and Azure AI Agent Service for this use case?
>
> A: AutoGen 被专门设计用于事件驱动、分布式的代理应用，使其非常适合自动化代码生成和数据分析任务。它提供构建复杂多代理系统所需的工具和能力，从而提高效率。

>Q: Sounds like Azure AI Agent Service could work here too, it has tools for code generation and more?

>
> A: 是的，Azure AI Agent Service 是一个代理的平台服务，并为多个模型、Azure AI Search、Bing Search 和 Azure Functions 添加了内置能力。它使您可以在 Foundry 门户中轻松构建代理并按规模部署它们。
 
> Q: I'm still confused just give me one option
>
> A: 一个很好的选择是先在 Semantic Kernel 中构建您的应用，然后使用 Azure AI Agent Service 部署您的代理。这种方法允许您轻松持久化代理，同时利用 Semantic Kernel 构建多代理系统的能力。此外，Semantic Kernel 在 AutoGen 中有一个连接器，使两者一起使用变得容易。
 
Let's summarize the key differences in a table:

| 框架 | 关注点 | 核心概念 | 使用场景 |
| --- | --- | --- | --- |
| AutoGen | 事件驱动、分布式的代理应用 | 代理、角色、函数、数据 | 代码生成、数据分析任务 |
| Semantic Kernel | 理解和生成类似人类的文本内容 | 代理、模块化组件、协作 | 自然语言理解、内容生成 |
| Azure AI Agent Service | 灵活的模型、企业安全、代码生成、工具调用 | 模块化、协作、流程编排 | 安全、可扩展且灵活的 AI 代理部署 |

What's the ideal use case for each of these frameworks?

## 我可以直接集成我现有的 Azure 生态系统工具，还是需要独立的解决方案？

答案是肯定的，您可以直接将现有的 Azure 生态系统工具与 Azure AI Agent 服务集成，尤其是因为它被构建为能够与其他 Azure 服务无缝配合。例如，您可以集成 Bing、Azure AI Search 和 Azure Functions。它还与 Microsoft Foundry 有深度集成。

对于 AutoGen 和 Semantic Kernel，您也可以与 Azure 服务集成，但这可能需要您在代码中调用 Azure 服务。另一种集成方式是使用 Azure SDK 从您的代理与 Azure 服务交互。此外，如前所述，您可以将 Azure AI Agent 服务用作由 AutoGen 或 Semantic Kernel 构建的代理的编排器，从而轻松访问 Azure 生态系统。

## 示例代码

- Python: [代理框架](./code_samples/02-python-agent-framework.ipynb)
- .NET: [代理框架](./code_samples/02-dotnet-agent-framework.md)

## 关于 AI Agent 框架还有更多问题？

加入 [Microsoft Foundry Discord](https://aka.ms/ai-agents/discord) 与其他学习者见面、参加答疑时段并获得您的 AI Agents 问题的解答。

## 参考资料

- <a href="https://techcommunity.microsoft.com/blog/azure-ai-services-blog/introducing-azure-ai-agent-service/4298357" target="_blank">Azure Agent 服务</a>
- <a href="https://devblogs.microsoft.com/semantic-kernel/microsofts-agentic-ai-frameworks-autogen-and-semantic-kernel/" target="_blank">Semantic Kernel 与 AutoGen</a>
- <a href="https://learn.microsoft.com/semantic-kernel/frameworks/agent/?pivots=programming-language-python" target="_blank">Semantic Kernel Python 代理框架</a>
- <a href="https://learn.microsoft.com/semantic-kernel/frameworks/agent/?pivots=programming-language-csharp" target="_blank">Semantic Kernel .Net 代理框架</a>
- <a href="https://learn.microsoft.com/azure/ai-services/agents/overview" target="_blank">Azure AI Agent 服务</a>
- <a href="https://techcommunity.microsoft.com/blog/educatordeveloperblog/using-azure-ai-agent-service-with-autogen--semantic-kernel-to-build-a-multi-agen/4363121" target="_blank">将 Azure AI Agent Service 与 AutoGen / Semantic Kernel 一起用于构建多代理解决方案</a>

## 上一课

[AI 代理与用例介绍](../01-intro-to-ai-agents/README.md)

## 下一课

[理解代理设计模式](../03-agentic-design-patterns/README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
免责声明：
本文件已使用 AI 翻译服务 Co-op Translator（https://github.com/Azure/co-op-translator）进行翻译。尽管我们力求准确，但请注意自动翻译可能包含错误或不准确之处。原始语言的原文应被视为权威来源。对于重要信息，建议采用专业人工翻译。因使用本翻译而产生的任何误解或错误解释，我们不承担责任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->
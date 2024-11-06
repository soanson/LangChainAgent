from langchain.agents import Tool, AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory


# 使用GoogleSerperAPIWrapper需要先到Serper官网注册登录
# 然后设置以下环境变量为你的API key
import os

from langchain_community.utilities import SerpAPIWrapper
from langchain_openai import ChatOpenAI

os.environ["SERPAPI_API_KEY"] = "cfe4242ca57fac7a016555c8ea000e9a58def10692e08f7f8c5cddf6b79d5ae6"



search =  SerpAPIWrapper()
tools = [
    Tool(
        name='search',
        func=search.run,
        description='用于搜索当前事件'
    )
]
memory = ConversationBufferMemory(
    memory_key='chat_history',
    return_messages=True
)

llm = ChatOpenAI(model_name='gpt-4-1106-preview',temperature=0)
agent = initialize_agent(
    tools, llm,
    # CHAT_CONVERSATIONAL_REACT_DESCRIPTION用于聊天类型模型
    # CONVERSATIONAL_REACT_DESCRIPTION用于LLM补全模型
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)
agent.run(input='小张今年25岁。')
agent.run(input='现任微软公司CEO的年龄是多少')
print(agent.run('现任OpenAI公司CEO的年龄是多少？两位CEO的年龄加上小张的年龄，这三人的年龄和等于多少？'))
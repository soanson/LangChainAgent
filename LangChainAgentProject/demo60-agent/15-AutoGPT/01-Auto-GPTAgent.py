from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory

from langchain_community.utilities import SerpAPIWrapper
from langchain_experimental.autonomous_agents import AutoGPT
from langchain.tools.file_management.read import ReadFileTool
from langchain.tools.file_management.write import WriteFileTool

import os

from langchain_openai import ChatOpenAI

os.environ["SERPAPI_API_KEY"] = "cfe4242ca57fac7a016555c8ea000e9a58def10692e08f7f8c5cddf6b79d5ae6"

search = SerpAPIWrapper()
tools = [
    Tool(
        name='search',
        func=search.run,
        description='useful for when you need to '
                    'answer questions about current events. '
                    'You should ask targeted questions',
    ),
    WriteFileTool(),
    ReadFileTool(),
]
"""
embedding = OpenAIEmbeddings()
vectorstore = Chroma(
    persist_directory='./chroma',
    embedding_function=embedding
)
"""

#记忆组件
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)
agent = AutoGPT.from_llm_and_tools(
    ai_name='Tom',
    ai_role='Assistant',
    tools=tools,
    llm=ChatOpenAI(
        model_name='gpt-4-1106-preview',
        temperature=0
    ),
    memory=memory,
)

# 打开详情模式
agent.chain.verbose = True

# 生成一个关于今天杭州天气的中文报告
agent.run([
    'Please help me write a Chinese report on '
    'the weather in Hangzhou today, in which the '
    'temperature unit needs to be in Celsius and '
    'saved as "hangzhou_weather.txt"'
])
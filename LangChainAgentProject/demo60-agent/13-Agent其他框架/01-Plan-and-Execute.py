from langchain_core.tools import Tool

from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
from langchain import SerpAPIWrapper
from langchain import LLMMathChain
#from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

#load_dotenv()
import os
os.environ["SERPAPI_API_KEY"] = "cfe4242ca57fac7a016555c8ea000e9a58def10692e08f7f8c5cddf6b79d5ae6"

"""
计划与执行（Plan-and-Execute）框架侧重于先规划一系列的行动，然后执行。
这个框架可以使大模型能够先综合考虑任务的多个方面，然后按照计划进行行动。
应用在比较复杂的项目管理中或者需要多步决策的场景下会比较合适。
"""
# 配置API密钥和基础URL
llm = ChatOpenAI()

# 创建工具
search = SerpAPIWrapper()  # 请替换为你的SerpAPI API密钥
llm_math_chain = LLMMathChain(llm=llm, verbose=True)

# 定义工具列表
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="用于回答关于当前事件的问题"
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="用于计算或解决问题"
    )
]

# 加载规划器和执行器
planner = load_chat_planner(llm)
executor = load_agent_executor(llm, tools, verbose=True)

# 创建Plan and Execute代理
agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)

# 运行代理解决实际问题
print(agent.run("在北京，100元能买几个肯德基的汉堡，请用中文回答？"))
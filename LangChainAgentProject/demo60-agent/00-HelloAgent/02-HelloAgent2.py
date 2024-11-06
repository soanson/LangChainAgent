from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, load_tools
from langchain.agents import AgentType
#from langchain_community.agent_toolkits.load_tools import load_tools
import os
os.environ["SERPAPI_API_KEY"] = "cfe4242ca57fac7a016555c8ea000e9a58def10692e08f7f8c5cddf6b79d5ae6"

#定义llm
llm = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo",
)


tools = load_tools(["serpapi","llm-math"], llm=llm)

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,#这里有不同的类型
    verbose=True,#是否打印日志
    handle_parsing_errors=True
)

#print(agent.run("请问现任的OpenAI公司  CEO是谁？他的年龄的是多少? 现任微软CEO的年龄，加上OpenAI CEO年龄之和，请用中文告诉我这三个问题的答案"))
print(agent.run("2023年微软CEO出生于哪个国家？这个国家首都距离北京多少公里？最后得到的结果是多少？"))
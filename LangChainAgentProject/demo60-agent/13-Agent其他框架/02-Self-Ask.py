import os
from langchain import hub
from langchain.agents import AgentExecutor, create_self_ask_with_search_agent
from langchain_community.tools.tavily_search import TavilyAnswer
#from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

#load_dotenv()
# 配置模型


tools = []
#获取prompt
prompt = hub.pull("hwchase17/self-ask-with-search")
print(prompt)
# 配置API密钥和基础URL
llm = ChatOpenAI()
agent = create_self_ask_with_search_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True,handle_parsing_errors=True)
print(agent_executor.invoke({"input": "上一届的美国总统是谁?"}))

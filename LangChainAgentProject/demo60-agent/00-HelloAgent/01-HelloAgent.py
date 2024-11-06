
#from langchain_community.agent_toolkits.load_tools import load_tools
from langchain import hub
from langchain.agents import create_structured_chat_agent, AgentExecutor, load_tools
from langchain_openai import ChatOpenAI

#pip install -U duckduckgo-search
#pip install numexpr
#pip install langchain_community
#pip install langchainhub

#from EnvUtils import setAPIKeyAndBaseURL
#setAPIKeyAndBaseURL()

llm = ChatOpenAI(
    model_name='gpt-4o',
    temperature=0.6
)
# Set the BING_SUBSCRIPTION_KEY environment variable
import os
os.environ["BING_SUBSCRIPTION_KEY"] = "e1552b26-d384-4b3d-9548-bddbacb14129"

tools = load_tools(['ddg-search', 'llm-math'], llm=llm)
#tools = load_tools(['bing-search', 'llm-math'], llm=llm)

prompt = hub.pull("hwchase17/structured-chat-agent")
print(prompt)

agent = create_structured_chat_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools,  return_intermediate_steps=True, verbose=True, handle_parsing_errors=True
)

print(agent_executor.invoke({"input":'第2届百度开发者大会召开的年份除以4,然后平方，最后得到的数字是多少？'}))

#print(agent_executor.invoke({"input":'请一步一步思考，今年是2024年，张明在中国成立时4岁，他哥哥比他大3岁，请问他哥哥明年几岁，最后得到的数字是多少？'}))


#print(agent_executor.invoke({"input":'2023年微软CEO出生于哪个国家？这个国家首都距离北京多少公里？最后得到的结果是多少？'}))
#print(agent_executor.invoke({"input":'小明今年10岁，上小学3年级，在学习python编程,准备学习二分查找，请你给出代码，并且解析代码含义，最后给出数组[2,6,9,10,45,89],如何使用函数查询数字10，最后获得10在数组的位置是多少？'}))
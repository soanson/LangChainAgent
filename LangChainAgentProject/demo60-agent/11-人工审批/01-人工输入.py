from langchain.agents import AgentType, load_tools
from langchain.agents import initialize_agent
#from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.callbacks import HumanApprovalCallbackHandler
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(
    model_name='gpt-4-1106-preview',
    temperature=0
)
tools = load_tools(['human', 'llm-math'], llm=llm)

agent = initialize_agent(
    tools, llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    # 如果出现结果解析错误，可以将handle_parsing_errors设置为True
    handle_parsing_errors=True,
    verbose=True
)
print(agent.run(
    '请先让用户一次性输入两个值（用逗号隔开），然后对这两个值进行加法运算'
))
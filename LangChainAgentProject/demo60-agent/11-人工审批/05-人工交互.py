from langchain.agents import AgentType, load_tools
from langchain.agents import initialize_agent
#from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.callbacks import HumanApprovalCallbackHandler
from langchain_openai import ChatOpenAI


def _should_check(serialized_obj: dict) -> bool:
    # 当工具名称为terminal时，需要进行审批
    return serialized_obj.get('name') == 'terminal'


def _approve(_input: str) -> bool:
    if _input == 'echo "Hello World"':
        return True
    msg = (
        '是否批准执行以下输入？'
        '回复Y或者yes为批准，回复其他内容则视为不批准。'
    )
    msg += '\n\n' + _input + '\n'
    resp = input(msg)
    return resp.lower() in ('yes', 'y')


callbacks = [
    HumanApprovalCallbackHandler(
        should_check=_should_check,
        approve=_approve
    )]

llm = ChatOpenAI(temperature=0)
tools = load_tools(['wikipedia', 'llm-math', 'terminal'], allow_dangerous_tools=True,llm=llm)
agent = initialize_agent(
    tools, llm,handle_parsing_errors=True,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
)

res = agent.run('秦朝统一六国是哪一年？', callbacks=callbacks)
print(res)
res = agent.run('请列出当前目录下的文件', callbacks=callbacks)
print(res)
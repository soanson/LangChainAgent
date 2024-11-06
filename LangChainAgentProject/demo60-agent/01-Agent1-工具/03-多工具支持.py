from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def multiply(first_int: int, second_int: int) -> int:
    """Multiply two integers together."""
    return first_int * second_int

@tool
def add(first_int: int, second_int: int) -> int:
    "Add two integers."
    return first_int + second_int

@tool
def exponentiate(base: int, exponent: int) -> int:
    "Exponentiate the base to the exponent power."
    return base**exponent

print(multiply.name)
print(multiply.description)
print(multiply.args)

from langchain_experimental.tools import PythonREPLTool
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

# Initialize Python REPL Tool
pythonREPLTool = PythonREPLTool()

# Initialize Wikipedia API Wrapper
wikipedia_api = WikipediaAPIWrapper()

# Define Wikipedia Query Run Tool
wikipedia = Tool(
    name='WikipediaQueryRun',
    func=wikipedia_api.run,
    description='useful for when you need to ask with Wikipedia'
)

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import Tool

# Initialize DuckDuckGo Search Run Tool
search = Tool(
    name='DuckDuckGoSearchRun',
    func=DuckDuckGoSearchRun().run,
    description='useful for when you need to ask with DuckDuckGo search'
)

from langchain import hub
prompt = hub.pull("hwchase17/structured-chat-agent")
prompt.pretty_print()

#定义工具
tools = [pythonREPLTool, wikipedia, search, multiply, add, exponentiate]

llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)

from langchain.agents import create_structured_chat_agent
# 创建 structured chat agent
agent = create_structured_chat_agent(llm, tools, prompt)

from langchain.agents import AgentExecutor
# 传入agent和tools来创建Agent执行器
agent_executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True, verbose=True)

agent_executor.invoke(
    {
        "input": "Take 3 to the fifth power and multiply that by the sum of twelve and three, then square the whole result"
    }
)

agent_executor.invoke(
    {
        "input": "美团上一个交易日的股票价格是多少？"
        #"input": "OpenAI公司CEO 是多谁？  他毕业于那所大学？ 出生在哪里？"
    }
)
agent_executor.invoke(
    {
        "input": "迈克尔乔丹生日多少?"
    }
)
agent_executor.invoke(
    {
        "input": "HUNTER X HUNTER是什么?"
    }
)

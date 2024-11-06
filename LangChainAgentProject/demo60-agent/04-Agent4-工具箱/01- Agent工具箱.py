from langchain import hub
from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.tools import BaseTool, Tool
from langchain_experimental.agents.agent_toolkits import create_csv_agent, create_python_agent
from langchain_experimental.tools import PythonREPLTool
from langchain_openai import ChatOpenAI


model = ChatOpenAI(model='gpt-3.5-turbo')

class TextLengthTool(BaseTool):
    name = "文本字数计算工具"
    description = "当你需要计算文本包含的字数时，使用此工具"

    def _run(self, text):
        return len(text)



python_agent_executor = create_python_agent(
    llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
    tool=PythonREPLTool(),
    verbose=True,
    allow_dangerous_code=True,  # 允许执行危险代码
    agent_executor_kwargs={"handle_parsing_errors": True}
)

csv_agent_executor = create_csv_agent(
    llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0,),
    path="../03-Agent3-分析数据/house_price.csv",
    verbose=True,
    allow_dangerous_code=True,  # 允许执行危险代码
    agent_executor_kwargs={"handle_parsing_errors": True}
)

tools=[
    Tool(
        name="Python代码工具",
        description="""当你需要借助Python解释器时，使用这个工具。
        用自然语言把要求给这个工具，它会生成Python代码并返回代码执行的结果。""",
        func=python_agent_executor.invoke
    ),
    Tool(
        name="CSV分析工具",
        description="""当你需要回答有关house_price.csv文件的问题时，使用这个工具。
        它接受完整的问题作为输入，在使用Pandas库计算后，返回答案。""",
        func=csv_agent_executor.invoke
    ),
    TextLengthTool()
]

memory = ConversationBufferMemory(
    memory_key='chat_history',
    return_messages=True
)
prompt = hub.pull("hwchase17/structured-chat-agent")
print(prompt)

agent = create_structured_chat_agent(
    llm=model,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)

agent_executor.invoke({"input": "第8个斐波那契数列的数字是多少？"})

agent_executor.invoke({"input": "house_price数据集里，所有房子的价格平均值是多少？用中文回答"})

agent_executor.invoke({"input": "'君不见黄河之水天上来奔流到海不复回'，这句话的字数是多少？"})


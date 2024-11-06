from langchain_community.docstore import Wikipedia
#from langchain_community.agent_toolkits.load_tools import load_tools
from langchain import hub
from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

# Initialize the Wikipedia docstore
docstore = Wikipedia()

# Initialize Search tool
tools = [
    Tool(
        name='Search',
        func=docstore.search,
        description='useful for when you need to ask with search',
    ),
    # Remove or replace the Lookup tool if not available
    # Tool(
    #     name='Lookup',
    #     func=docstore.lookup,
    #     description='useful for when you need to ask with lookup',
    # ),
]

llm = ChatOpenAI(
    model_name='gpt-4o',
    temperature=0.6
)

# Pull the prompt from the hub
prompt = hub.pull("hwchase17/structured-chat-agent")

# Create the structured chat agent
agent = create_structured_chat_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, return_intermediate_steps=True, verbose=True, handle_parsing_errors=True
)

print(agent_executor.invoke({"input": '秦朝建立是在什么时间？'}))
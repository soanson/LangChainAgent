
from langchain_experimental.agents.agent_toolkits import create_python_agent
from langchain_experimental.tools import PythonREPLTool
from langchain_openai import ChatOpenAI

#pip install langchain_experimental

tools = [PythonREPLTool()]
agent_executor = create_python_agent(
    llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
    tool=PythonREPLTool(),
    verbose=True,
    agent_executor_kwargs={"handle_parsing_errors": True}
)

print(agent_executor.get_prompts())

#agent = create_python_agent(llm, tool=PythonREPLTool(), verbose=True)

customer_list = [
    ["Harrison", "Chase"],
    ["Lang", "Chain"],
    ["Dolly", "Too"],
    ["Elle", "Elem"],
    ["Geoff", "Fusion"],
    ["Trance", "Former"],
    ["Jen", "Ayai"],
]

agent_executor.invoke(  f"""Sort these customers by
last name and then first name
and print the output: {customer_list}"""
)
from langchain import hub
from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from datetime import date

#from EnvUtils import setAPIKeyAndBaseURL
#setAPIKeyAndBaseURL()


class DateTimeTool(BaseTool):
    name = "Returns todays date"
    description = """Returns todays date, use this for any
           questions related to knowing todays date.
           The input should always be an empty string,
           and this function will always return todays
           date - any date mathmatics should occur
           outside this function."""

    def _run(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")


model = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)


tools = [DateTimeTool()]
prompt = hub.pull("hwchase17/structured-chat-agent")
print(prompt)

agent = create_structured_chat_agent(
    llm=model,
    tools=tools,
    prompt=prompt
)

memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
)
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, memory=memory, verbose=True, handle_parsing_errors=True
)
result2=agent_executor.invoke({"input": "whats the date today?"})
print(result2)


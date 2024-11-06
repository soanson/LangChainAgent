from langchain import hub
from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI

#from EnvUtils import setAPIKeyAndBaseURL
#setAPIKeyAndBaseURL()


class TextLengthTool(BaseTool):
    name = "文本字数计算工具"
    description = "当你被要求计算文本的字数时，使用此工具"

    def _run(self, text):
        print("使用文本字数计算工具 " )
        #print(text)
        #print("使用文本字数计算工具 ")
        return len(text)

model = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)


tools = [TextLengthTool()]
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
result2=agent_executor.invoke({"input": "'君不见黄河之水天上来奔流到海不复回'，这句话的字数是多少？"})
print(result2)

result2=agent_executor.invoke({"input": "'The prompt can be use as shown below'，这句话的字数是多少？"})
print(result2)

result3=agent_executor.invoke({"input": "请你充当我的物理老师，告诉我什么是量子力学"})
print(result3)
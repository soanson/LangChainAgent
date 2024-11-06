

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

#print(agent_executor.invoke({"input": "7的2.3次方是多少？"}))
#print(agent_executor.invoke({"input": "第12个斐波那契数列的数字是多少？"}))
#print(agent_executor.invoke({"input": "在数组中使用二分查找数字，请在[2,4,5,9,10,13,17,20,28]数组使用二分查询17， 这个17在数组中位置是几 ？"}))
print(agent_executor.invoke({"input": "在数组中使用冒泡排序，请对[12,44,15,19,10,113,107,20,28]数组进行冒泡排序， 请输出排序过程中每一伦后的数组信息，最后输出排序后的数组内容 ？"}))



from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI



agent_executor = create_csv_agent(
    llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0,),
    path="house_price.csv",
    verbose=True,
    allow_dangerous_code=True,  # 允许执行危险代码
    agent_executor_kwargs={"handle_parsing_errors": True}
)

print(agent_executor)
#print(agent_executor.invoke({"input": "数据集有多少行，多少列？用中文回复"}))


#agent_executor.invoke({"input": "数据集包含哪些变量？用中文回复"})


#agent_executor.invoke({"input": "数据集里，所有房子的价格平均值是多少？用中文回复"})

agent_executor.invoke({"input": "数据集里，所有房子的装修状态包含哪些种类？你认为它们具体表示什么意思？用中文回复"})



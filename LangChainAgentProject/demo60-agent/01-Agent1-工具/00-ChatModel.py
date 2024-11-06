
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI

#from EnvUtils import setAPIKeyAndBaseURL
#setAPIKeyAndBaseURL()



model = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)

result=model.invoke([HumanMessage(content="'君不见黄河之水天上来奔流到海不复回'，这句话的字数是多少？")])
print(result)


result=model.invoke([HumanMessage(content="'The prompt can be use as shown below'，这句话的字数是多少？")])
print(result)

result3=model.invoke("请你充当我的物理老师，告诉我什么是量子力学")
print(result3)

result3=model.invoke("请问今天北京天气多少？")
print(result3)




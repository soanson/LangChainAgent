from langchain.prompts import PromptTemplate  # 用于构建提示词模板
from langchain_openai import ChatOpenAI

from EnvUtils import setAPIKeyAndBaseURL
setAPIKeyAndBaseURL()

llm = ChatOpenAI(model_name='gpt-4o-mini')

template = '写一首描写{sence}的诗'
prompt = PromptTemplate.from_template(template)

chain = prompt | llm  # 类似 Linux的管道操作，前一个的输出，作为下一个的输入

result = chain.invoke({'sence': '秋天'})
print(result)

# content='秋风轻拂树梢间，\n金黄的叶片飘落满山坡。\n清晨的露珠凝满叶，\n晚霞映照天边的波。




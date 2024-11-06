import os
import operator
import functools
from typing import Annotated, Sequence, TypedDict

from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser

from langgraph.graph import StateGraph, END
import os
os.environ["SERPAPI_API_KEY"] = "cfe4242ca57fac7a016555c8ea000e9a58def10692e08f7f8c5cddf6b79d5ae6"


@tool('web_search')
def web_search(query):
    """通过Google SERP API进行互联网搜索查询"""
    search = SerpAPIWrapper()
    return search.run(query)


@tool('red_book_writer')
def write_red_book(content):
    """根据一段内容，写一个小红书文案"""
    chat = ChatOpenAI(model='gpt-4-turbo-preview')
    system_msg = SystemMessage(
        content='你的任务是以小红书博主的文章结构，以我给出的主题，写一篇推荐帖。'
                '你的回答应包括使用表情符号来增加趣味和互动，'
                '以及与每个段落相匹配的图片。'
                '请以一个引人入胜的介绍开始，为你的推荐帖设置基调。'
                '然后，提供至少3个与主题相关的段落，突出它们的特点和吸引力。'
                '在你的写作中使用表情符号，使文案更加引人入胜和有趣。'
    )
    messages = [
        system_msg,
        HumanMessage(content=content),
    ]
    response = chat(messages)
    return response.content

system_prompt = (
    'You are a supervisor tasked with managing a conversation between the'
    ' following workers:  {members}. Given the following user request,'
    ' respond with the worker to act next. Each worker will perform a'
    ' task and respond with their results and status. When finished,'
    ' respond with FINISH.'
)

members = ['Search_Engine', 'Red_Book_Writer']
options = ['FINISH'] + members


# 使用OpenAI的函数调用，可以更方便地输出一个结构化的内容
func_structure = {
    'name': 'route',
    'description': 'Select the next role.',
    'parameters': {
        'title': 'routeSchema',
        'type': 'object',
        'properties': {
            'next': {
                'title': 'Next',
                'anyOf': [
                    {'enum': options},
                ],
            }
        },
        'required': ['next'],
    },
}
prompt = ChatPromptTemplate.from_messages(
    [
        ('system', system_prompt),
        MessagesPlaceholder(variable_name='messages'),
        (
            'system',
            'Given the conversation above, who should act next?'
            ' Or should we FINISH? Select one of: {options}',
        ),
    ]
).partial(options=str(options), members=', '.join(members))

llm = ChatOpenAI(model='gpt-4-turbo-preview')
supervisor_chain = (
    prompt
    | llm.bind_functions(functions=[func_structure], function_call='route')
    | JsonOutputFunctionsParser()
)

def create_agent(llm, tools, system_prompt):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                'system',
                system_prompt,
            ),
            MessagesPlaceholder(variable_name='messages'),
            MessagesPlaceholder(variable_name='agent_scratchpad'),
        ]
    )
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor


def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {'messages': [HumanMessage(content=result['output'], name=name)]}


search_engine_agent = create_agent(
    llm,
    [web_search],
    '你是一个网络搜索引擎'
)
search_engine_node = functools.partial(
    agent_node,
    agent=search_engine_agent,
    name='Search_Engine'
)

red_book_agent = create_agent(
    llm,
    [write_red_book],
    '你的主要职责是根据给定的内容编写小红书文案。'
)
red_book_node = functools.partial(
    agent_node,
    agent=red_book_agent,
    name='Red_Book_Writer'
)

# 状态对象存储了两个字段：
# messages用于保存上游处理完的信息
# next用于记录要执行哪个下游节点
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str

workflow = StateGraph(AgentState)
workflow.add_node('Search_Engine', search_engine_node)
workflow.add_node('Red_Book_Writer', red_book_node)
workflow.add_node('supervisor', supervisor_chain)

# 这里实际上添加的代码逻辑是，执行完对应的节点再回到supervisor节点
for member in members:
    workflow.add_edge(member, 'supervisor')

conditional_map = {k: k for k in members}
conditional_map['FINISH'] = END
workflow.add_conditional_edges(
    'supervisor',
    lambda x: x['next'],
    conditional_map
)

# 设置起始节点
workflow.set_entry_point('supervisor')
graph = workflow.compile()

for s in graph.stream({
    'messages': [
        HumanMessage(
            content='请先搜索OpenAI的Sora，并根据搜索结果写一篇小红书文案'
        )
    ]
}):
    if '__end__' not in s:
        print(s)
        print('----')
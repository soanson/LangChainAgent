from langchain_openai import ChatOpenAI



llm = ChatOpenAI(
    temperature=0,
    model="gpt-4",
)
#from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent, load_tools

tools = load_tools(["dalle-image-generator"])
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True
)
# 这是一只可爱的英国短毛小猫的特写，圆脸，大眼睛，蓬松的金棕色皮毛，腹部较浅。小猫有小而圆的耳朵，粉红色的鼻子和黑色的爪垫。它躺在柔软的、有纹理的表面上，好奇地微微倾斜着头，向上凝视着。背景稍微模糊，将焦点集中在小猫可爱的特征上，整体氛围温暖舒适。
output = agent.run("A close-up portrait of an adorable British Shorthair kitten with a round face, big expressive eyes, and a fluffy, golden-brown fur coat with a lighter underbelly. The kitten has small, rounded ears, a pink nose, and black paw pads. It is lying down on a soft, textured surface, with a curious and slightly tilted head, gazing upwards. The background is slightly blurred, drawing focus to the kitten's cute features, and the overall atmosphere is warm and cozy.")
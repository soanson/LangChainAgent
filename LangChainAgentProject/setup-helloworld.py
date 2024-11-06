import os
from openai import OpenAI

"""
To install the official Python bindings, run the following command:
pip install openai
"""

from EnvUtils import setAPIKeyAndBaseURL
setAPIKeyAndBaseURL()

client = OpenAI()


response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "你好，请介绍你自己？"}
  ]
)
print(response)
print(response.choices[0].message.content)




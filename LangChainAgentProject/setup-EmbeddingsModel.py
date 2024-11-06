
from langchain_openai import OpenAIEmbeddings

from EnvUtils import setAPIKeyAndEmbeddingBaseURL
setAPIKeyAndEmbeddingBaseURL()
model="text-embedding-3-small-deploy"

#text-embedding-3-small
#text-embedding-3-large

embeddings_model = OpenAIEmbeddings(model=model)


embeded_result = embeddings_model.embed_documents(["Hello world!", "Hey bro"])
print(len(embeded_result))
print(embeded_result)




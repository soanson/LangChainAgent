


import os
import requests


def getBaseURL():
    #return 'https://mlop-llm-gateway-dev.home-np.oocl.com/engines/gpt-4o-mini-deploy-gs/'
    return  'https://mlop-llm-gateway-dev.home-np.oocl.com/engines/gpt-4o-240806-deploy-gs/'

def getEmbeddingBaseURL():
    return 'https://mlop-llm-gateway-dev.home-np.oocl.com/engines/text-embedding-3-small-deploy/'

def getAPIKey():
    # Keycloak服务器信息
    keycloak_token_url = "https://iamfw.home-np.oocl.com/auth/realms/oocl-dev/protocol/openid-connect/token"
    client_id = "ai-competition-2024"
    client_secret = "mufE79Yp9648hB3ObZAbnikhkfoFNGVe"

    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    response = requests.post(keycloak_token_url, data=data)
    if response.status_code == 200:
        token = response.json()["access_token"]
        #print(f"Access token: {token}")
        return  token

    return "error"

#设置公司网关和API KEY
def setAPIKeyAndBaseURL():
    os.environ['OPENAI_API_KEY'] = getAPIKey()
    os.environ['OPENAI_BASE_URL'] = getBaseURL()
    print("***OPENAI_API_KEY****")
    print(os.environ['OPENAI_API_KEY'])
    print("****OPENAI_BASE_URL ***")
    print(os.environ['OPENAI_BASE_URL'])

#设置公司Embedding网关和API KEY
def setAPIKeyAndEmbeddingBaseURL():
    os.environ['OPENAI_API_KEY'] = getAPIKey()
    os.environ['OPENAI_BASE_URL'] = getEmbeddingBaseURL()
    print("***OPENAI_API_KEY****")
    print(os.environ['OPENAI_API_KEY'])
    print("****OPENAI_BASE_URL （EmbeddingBaseURL）***")
    print(os.environ['OPENAI_BASE_URL'])





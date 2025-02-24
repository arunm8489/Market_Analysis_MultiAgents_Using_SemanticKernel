import os 
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
from azure.identity import ClientSecretCredential, get_bearer_token_provider
from openai import AzureOpenAI


load_dotenv()

def get_openai_client():

    credential = ClientSecretCredential(
        os.getenv("OPENAI_AD_TENANT_ID"), 
        os.getenv("OPENAI_AD_CLIENT_ID"), 
        os.getenv("OPENAI_AD_CLIENT_SECRET")
    )

    token_provider = get_bearer_token_provider(
        credential, "https://cognitiveservices.azure.com/.default"
    )

    openai_client = AsyncAzureOpenAI(
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv('OPENAI_API_BASE'),
        azure_ad_token_provider=token_provider,
    )

    return openai_client


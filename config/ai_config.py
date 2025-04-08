import openai, os
from dotenv import load_dotenv

load_dotenv()

def get_openai():
    client = openai.AzureOpenAI(
    azure_endpoint="https://fyp2025.openai.azure.com",
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2024-02-01"
)
    return client
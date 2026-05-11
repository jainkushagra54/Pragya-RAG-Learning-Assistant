import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def get_embedding_function():
    return GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2",
        google_api_key=os.getenv("API_KEY")
    )
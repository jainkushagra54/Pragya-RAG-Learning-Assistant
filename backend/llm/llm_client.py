from google import genai
import os
from dotenv import load_dotenv
from pathlib import Path
import time

envpath = Path(__file__).resolve().parent.parent/".env"

load_dotenv(dotenv_path=envpath)

API_KEY = os.getenv("API_KEY")

client = genai.Client(
    api_key= API_KEY
)

def query_llm(prompt: str):
    print("Sent to Gemini")
    start_time = time.time()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    end_time = time.time()
    latency = round(end_time - start_time , 2)
    print(response.text)

    return {
        "answer": response.text,
        "latency":latency
    }
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from rag.query_data_llm import query_rag
from rag.populatedb import ingest_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = "data"
os.makedirs(DATA_PATH, exist_ok=True)

@app.post("/process")
async def process(files: list[UploadFile] = File([]), youtube: str = Form(None)):

    for file in files:
        file_path = os.path.join(DATA_PATH, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    if youtube:
        with open("youtube_links.txt", "a") as f:
            f.write(youtube + "\n")

    ingest_data(reset=False)

    return {"status": "processed"}


@app.post("/query")
async def query(data: dict):
    question = data.get("question")

    result = query_rag(question)

    return result
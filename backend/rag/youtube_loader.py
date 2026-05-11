import requests
from langchain_classic.schema.document import Document
import os

def extract_video_id(url: str) -> str:
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1]
    else:
        raise ValueError("Invalid YouTube URL")


def load_youtube_transcript(url: str, chunk_size=800):
    video_id = extract_video_id(url)

    api_key = os.getenv("SUPADATA_API_KEY")
    response = requests.get(
        f"https://api.supadata.ai/v1/youtube/transcript",
        params={"videoId": video_id, "text": True},
        headers={"x-api-key": api_key}
    )

    data = response.json()
    content = data.get("content", "")

    if isinstance(content, list):
        full_text = " ".join([item.get("text", "") for item in content])
    else:
        full_text = content

    if not full_text:
        raise ValueError("No transcript found")

    documents = []
    buffer_text = ""
    words = full_text.split()

    for i, word in enumerate(words):
        buffer_text += " " + word
        if len(buffer_text) >= chunk_size:
            documents.append(
                Document(
                    page_content=buffer_text.strip(),
                    metadata={
                        "source": url,
                        "type": "youtube",
                        "timestamp": 0,
                        "video_id": video_id,
                    },
                )
            )
            buffer_text = ""

    if buffer_text:
        documents.append(
            Document(
                page_content=buffer_text.strip(),
                metadata={
                    "source": url,
                    "type": "youtube",
                    "timestamp": 0,
                    "video_id": video_id,
                },
            )
        )

    return documents
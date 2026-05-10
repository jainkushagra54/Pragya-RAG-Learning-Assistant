from youtube_transcript_api import YouTubeTranscriptApi
from langchain_classic.schema.document import Document


def extract_video_id(url: str) -> str:
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1]
    else:
        raise ValueError("Invalid YouTube URL")


def load_youtube_transcript(url: str, chunk_size=800):
    video_id = extract_video_id(url)

    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id)

    documents = []
    buffer_text = ""
    start_time = None

    for entry in transcript:
        text = entry.text.strip()

        if not text:
            continue

        if start_time is None:
            start_time = int(entry.start)

        buffer_text += " " + text

        if len(buffer_text) >= chunk_size:
            documents.append(
                Document(
                    page_content=buffer_text.strip(),
                    metadata={
                        "source": url,
                        "type": "youtube",
                        "timestamp": start_time,
                        "video_id": video_id,
                    },
                )
            )
            buffer_text = ""
            start_time = None

    if buffer_text:
        documents.append(
            Document(
                page_content=buffer_text.strip(),
                metadata={
                    "source": url,
                    "type": "youtube",
                    "timestamp": start_time or 0,
                    "video_id": video_id,
                },
            )
        )

    return documents
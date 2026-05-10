import argparse
import os
import shutil

from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma

from rag.get_embedding_function import get_embedding_function
from rag.youtube_loader import load_youtube_transcript

CHROMA_PATH = "chroma"
DATA_PATH = "data"
YOUTUBE_FILE = "rag/youtube_links.txt"


def ingest_data(reset=False):
    if reset:
        print("✨ Clearing Database")
        clear_database()

    pdf_docs = load_pdf_documents()
    yt_docs = load_youtube_documents()

    documents = pdf_docs + yt_docs

    chunks = split_documents(documents)
    add_to_chroma(chunks)

def load_pdf_documents():
    loader = PyPDFDirectoryLoader(DATA_PATH)
    return loader.load()


def load_youtube_documents():
    all_docs = []

    if not os.path.exists(YOUTUBE_FILE):
        return all_docs

    with open(YOUTUBE_FILE, "r") as f:
        links = f.readlines()

    for link in links:
        link = link.strip()
        if not link:
            continue

        try:
            docs = load_youtube_transcript(link)
            all_docs.extend(docs)
        except Exception as e:
            print(f"❌ Error loading {link}: {e}")

    return all_docs

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
    )

    final_chunks = []

    for doc in documents:
        if doc.metadata.get("type") == "youtube":
            final_chunks.append(doc)
        else:
            final_chunks.extend(splitter.split_documents([doc]))

    return final_chunks

def assign_chunk_ids(chunks):
    for i, chunk in enumerate(chunks):
        source = chunk.metadata.get("source", "unknown")

        if chunk.metadata.get("type") == "youtube":
            video_id = chunk.metadata.get("video_id", "vid")
            timestamp = chunk.metadata.get("timestamp", 0)

            chunk_id = f"youtube:{video_id}:{timestamp}:{i}"
        else:
            page = chunk.metadata.get("page", 0)
            chunk_id = f"{source}:{page}:{i}"

        chunk.metadata["id"] = chunk_id

    return chunks


def add_to_chroma(chunks):
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding_function()
    )

    chunks = assign_chunk_ids(chunks)

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])

    print(f"Existing documents: {len(existing_ids)}")

    new_chunks = [
        chunk for chunk in chunks
        if chunk.metadata["id"] not in existing_ids
    ]

    if new_chunks:
        print(f"👉 Adding new chunks: {len(new_chunks)}")
        ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=ids)
        db.persist()
    else:
        print("✅ No new documents")

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args()

    ingest_data(reset=args.reset)
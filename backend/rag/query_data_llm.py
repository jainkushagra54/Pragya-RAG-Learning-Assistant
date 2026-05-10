from backend.llm.llm_client import query_llm
import argparse

from langchain_community.vectorstores.chroma import Chroma
from langchain_classic.prompts import ChatPromptTemplate
# from langchain_community.llms.ollama import Ollama

from backend.rag.get_embedding_function import get_embedding_function

CHROMA_PATH = "backend/chroma"

PROMPT_TEMPLATE = """
You are a teaching assistant.

Answer ONLY using the provided context.

Instructions:
- Start with a short definition
- Then explain simply and intuitively
- Combine information from notes and YouTube naturally
- Rewrite in clean language (do not copy raw text)
- Keep the answer concise but meaningful
- Mention timestamps if YouTube content is used
- If the context is insufficient, say so clearly

Format:

Definition
<short definition>

Explanation
<simple explanation>

Key Points
- bullet points

Sources
- relevant sources used

Context:
{context}

Question:
{question}

Answer:
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str)
    args = parser.parse_args()

    query_rag(args.query_text)


def query_rag(query_text: str):
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding_function()
    )

    results = db.similarity_search_with_score(query_text, k=2)

    context_text = "\n\n---\n\n".join(
        [doc.page_content for doc, _ in results]
    )

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE).format(
        context=context_text,
        question=query_text
    )

    print("Thinking...")
    result = query_llm(prompt)
    response_text = result["answer"]
    latency = result["latency"]
    print("Got the Data")
    
    sources = []
    for doc, _ in results:
        if doc.metadata.get("type") == "youtube":
            video_id = doc.metadata.get("video_id")
            timestamp = doc.metadata.get("timestamp")
            link = f"https://youtube.com/watch?v={video_id}&t={timestamp}s"
            sources.append(link)
        else:
            sources.append(doc.metadata.get("id"))

    return {
        "answer": response_text,
        "sources": sources,
        "latency": latency
    }


if __name__ == "__main__":
    main()
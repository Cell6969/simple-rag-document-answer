import os
from dotenv import load_dotenv
import openai
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

load_dotenv()


COLLECTION_NAME = "example"

# Init Qdrant & embedder
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
qdrant_client = QdrantClient(host=os.getenv("QDRANT_HOST"), port=os.getenv("QDRANT_PORT"))

openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_openai(question: str, context: str) -> str:
    prompt = f"""
    Kamu adalah asisten yang membantu menjawab pertanyaan berdasarkan konteks yang diberikan.
    Jika jawaban tidak ditemukan di dalam konteks, cukup jawab: "Maaf, jawaban tidak ditemukan dalam dokumen."

    Konteks:
    {context}

    Pertanyaan: {question}
    Jawaban:
    """

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=500,
    )

    return response.choices[0].message.content.strip()



def get_answer(question: str, top_k: int = 3) -> str:
    query_vector = embedding_model.encode(question).tolist()

    search_result = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k
    )

    context = "\n".join([point.payload["text"] for point in search_result])

    return ask_openai(question, context)

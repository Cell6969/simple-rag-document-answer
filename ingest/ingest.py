import os
import uuid
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv

load_dotenv()

COLLECTION_NAME = "example"
DOCS_PATH = "data"

model = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient(host=os.getenv("QDRANT_HOST"), port=os.getenv("QDRANT_PORT"))

client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

for filename in os.listdir(DOCS_PATH):
    path = os.path.join(DOCS_PATH, filename)
    if not filename.endswith((".txt")):
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    embedding = model.encode(content).tolist()
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={"text": content, "filename": filename}
        )]
    )

print("✅ Document already ingested.")
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore

from config import QDRANT_API_KEY, QDRANT_COLLECTION, QDRANT_URL
from rag.embeddings import get_embeddings


def get_qdrant_client() -> QdrantClient:
    if QDRANT_URL:
        return QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY or None,
        )

    # Local persistent Qdrant; no server is required.
    return QdrantClient(path=".qdrant")


def ensure_collection(client: QdrantClient) -> None:
    if client.collection_exists(QDRANT_COLLECTION):
        return

    # all-mpnet-base-v2 produces 768-dimensional embeddings.
    client.create_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=VectorParams(
            size=768,
            distance=Distance.COSINE,
        ),
    )


def get_vectorstore() -> QdrantVectorStore:
    client = get_qdrant_client()
    ensure_collection(client)

    return QdrantVectorStore(
        client=client,
        collection_name=QDRANT_COLLECTION,
        embedding=get_embeddings(),
    )

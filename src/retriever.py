"""
Qdrant client, vector store, and RBAC filter helpers.
Stage 1: Dense Vector Retrieval (BAAI/bge-small-en-v1.5).
"""
from __future__ import annotations
import atexit
import warnings

from fastembed import TextEmbedding
from langchain_core.embeddings import Embeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance, VectorParams

from src.config import QDRANT_PATH, COLLECTION_NAME

EMBED_MODEL = "BAAI/bge-small-en-v1.5"
EMBED_DIM   = 384


class _FastEmbedWrapper(Embeddings):
    """Thin LangChain Embeddings wrapper around fastembed.TextEmbedding."""
    def __init__(self, model_name: str) -> None:
        self._model = TextEmbedding(model_name=model_name)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [v.tolist() for v in self._model.embed(texts)]

    def embed_query(self, text: str) -> list[float]:
        return list(self._model.embed([text]))[0].tolist()


embeddings = _FastEmbedWrapper(EMBED_MODEL)

_client: QdrantClient | None = None


def get_qdrant_client() -> QdrantClient:
    global _client
    if _client is None:
        _client = QdrantClient(path=QDRANT_PATH)
    return _client


def _create_payload_index(client: QdrantClient) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="metadata.allowed_roles",
            field_schema=models.KeywordIndexParams(
                type=models.KeywordIndexType.KEYWORD,
                is_tenant=True,  # co-locates same-role vectors on disk → faster filtered reads
            ),
        )


def reset_collection_schema(client: QdrantClient) -> None:
    """Drop and recreate collection schema with Dense vectors only."""
    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
    )
    _create_payload_index(client)


def get_vector_store() -> QdrantVectorStore:
    client = get_qdrant_client()
    if not client.collection_exists(COLLECTION_NAME):
        reset_collection_schema(client)

    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
    )


def rbac_filter(role: str) -> models.Filter:
    return models.Filter(
        must=[
            models.FieldCondition(
                key="metadata.allowed_roles",
                match=models.MatchAny(any=[role]),
            )
        ]
    )


def rbac_filter_multi_role(roles: list[str]) -> models.Filter:
    return models.Filter(
        must=[
            models.FieldCondition(
                key="metadata.allowed_roles",
                match=models.MatchAny(any=roles),
            )
        ]
    )


def add_documents_to_qdrant(docs) -> list[str]:
    return get_vector_store().add_documents(documents=docs)


def build_retriever(k: int = 3, user_role: str | None = None):
    search_kwargs: dict = {"k": k}
    if user_role and user_role.lower() != "admin":
        search_kwargs["filter"] = rbac_filter(user_role)
    return get_vector_store().as_retriever(search_kwargs=search_kwargs)


def close_qdrant_client() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None


atexit.register(close_qdrant_client)

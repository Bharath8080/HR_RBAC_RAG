"""
Qdrant client, Hybrid Vector Store (Dense + BM25 Sparse) & RBAC filter helpers.
Stage 2: Hybrid Retrieval — Dense (BAAI/bge-small-en-v1.5) + Sparse (Qdrant/bm25).
"""
from __future__ import annotations
import atexit
import warnings

from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance, VectorParams, SparseVectorParams

from src.config import QDRANT_PATH, COLLECTION_NAME

# ── Model Config ──────────────────────────────────────────────────────────────
EMBED_MODEL        = "BAAI/bge-small-en-v1.5"
EMBED_DIM          = 384
SPARSE_MODEL       = "Qdrant/bm25"

# Named vector slots inside Qdrant collection
DENSE_VECTOR_NAME  = "dense"
SPARSE_VECTOR_NAME = "sparse"


# ── Embedding Singletons ─────────────────────────────────────────────────────
dense_embeddings  = FastEmbedEmbeddings(model_name=EMBED_MODEL)
sparse_embeddings = FastEmbedSparse(model_name=SPARSE_MODEL)


# ── Qdrant Client Singleton ───────────────────────────────────────────────────
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
    """Drop and recreate collection with Dense (cosine) + BM25 Sparse (IDF) vector slots."""
    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={
            DENSE_VECTOR_NAME: VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
        },
        sparse_vectors_config={
            SPARSE_VECTOR_NAME: SparseVectorParams(
                modifier=models.Modifier.IDF,  # proper BM25 IDF term-frequency weighting
            ),
        },
    )
    _create_payload_index(client)


def get_vector_store() -> QdrantVectorStore:
    """Return a QdrantVectorStore in HYBRID mode (Dense + BM25). Collection must exist."""
    client = get_qdrant_client()
    if not client.collection_exists(COLLECTION_NAME):
        reset_collection_schema(client)

    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=dense_embeddings,
        sparse_embedding=sparse_embeddings,
        retrieval_mode=RetrievalMode.HYBRID,
        vector_name=DENSE_VECTOR_NAME,
        sparse_vector_name=SPARSE_VECTOR_NAME,
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

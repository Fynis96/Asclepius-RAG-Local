from qdrant_client import QdrantClient, AsyncQdrantClient
from ..core.config import settings

def get_qdrant_client():
    return QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)

def get_async_qdrant_client():
    return AsyncQdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
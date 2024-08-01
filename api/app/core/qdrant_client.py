from qdrant_client import QdrantClient
from ..core.config import settings

def get_qdrant_client():
    return QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
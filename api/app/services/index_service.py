from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from ..core.qdrant_client import get_qdrant_client, get_async_qdrant_client
from ..crud.index import update_index_size
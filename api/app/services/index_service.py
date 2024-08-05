from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from ..core.qdrant_client import get_qdrant_client, get_async_qdrant_client
from ..core.minio_client import get_minio_client
from ..crud import index as crud_index
from ..crud import document as crud_document
from ..core.database import get_db
from ..core.config import settings
from sqlalchemy.orm import Session
import tempfile
import os
import asyncio
 
class IndexService:
    def __init__(self):
        self.minio_client = get_minio_client()
        self.qdrant_client = get_qdrant_client()
        self.async_qdrant_client = get_async_qdrant_client()
        self.db = next(get_db())

    async def create_index(self, index_id: int):
        db_index = crud_index.get_index(self.db, index_id)
        if not db_index:
            raise ValueError(f"Index with id {index_id} not found")

        collection_name = db_index.qdrant_collection_name

        # Delete collection if it exists
        if await self.async_qdrant_client.collection_exists(collection_name):
            await self.async_qdrant_client.delete_collection(collection_name)

        # Create vector store with hybrid indexing
        vector_store = QdrantVectorStore(
            collection_name,
            client=self.qdrant_client,
            aclient=self.async_qdrant_client,
            enable_hybrid=db_index.enabled_hybrid,
            batch_size=20,
            fastembed_sparse_model="Qdrant/bm42-all-minilm-l6-v2-attentions"
        )

        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        Settings.chunk_size = 512
        Settings.embed_model = HuggingFaceEmbedding(model_name=db_index.embed_model)

        documents = await self._load_documents(db_index.document_ids)

        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
        )

        # Update index size in the database
        new_size = len(documents)
        crud_index.update_index_size(self.db, index_id, new_size)

        return index

    async def _load_documents(self, document_ids: list[int]):
        documents = []
        with tempfile.TemporaryDirectory() as temp_dir:
            for doc_id in document_ids:
                try:
                    db_document = crud_document.get_document(self.db, doc_id)
                    if not db_document:
                        print(f"Document with id {doc_id} not found in the database.")
                        continue

                    file_obj = self.minio_client.get_object(settings.MINIO_BUCKET_NAME,
                        db_document.file_path)
                    file_path = os.path.join(temp_dir, db_document.filename)
                    with open(file_path, "wb") as f:
                        for d in file_obj.stream(32*1024):
                            f.write(d)

                    documents.extend(SimpleDirectoryReader(temp_dir).load_data())
                except Exception as e:
                    print(f"Error loading document {doc_id}: {str(e)}")

        return documents

    async def delete_index(self, index_id: int):
        db_index = crud_index.get_index(self.db, index_id)
        if not db_index:
            raise ValueError(f"Index with id {index_id} not found")

        collection_name = db_index.qdrant_collection_name

        if await self.async_qdrant_client.collection_exists(collection_name):
            await self.async_qdrant_client.delete_collection(collection_name)

        crud_index.delete_index(self.db, index_id)

    async def update_index(self, index_id: int):
        # This method can be implemented to update an existing index
        # It might involve deleting the old index and creating a new one
        await self.delete_index(index_id)
        await self.create_index(index_id)

    async def query_index(self, index_id: int, query: str):
        db_index = crud_index.get_index(self.db, index_id)
        if not db_index:
            raise ValueError(f"Index with id {index_id} not found")

        vector_store = QdrantVectorStore(
            db_index.qdrant_collection_name,
            client=self.qdrant_client,
            aclient=self.async_qdrant_client,
        )

        Settings.embed_model = HuggingFaceEmbedding(model_name=db_index.embed_model)

        index = VectorStoreIndex.from_vector_store(vector_store)
        query_engine = index.as_query_engine()
        response = await query_engine.aquery(query)
        return response

index_service = IndexService()
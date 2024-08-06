from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from ..core.qdrant_client import get_qdrant_client, get_async_qdrant_client
from ..core.minio_client import get_minio_client
from ..crud import index as crud_index
from ..crud import document as crud_document
from ..crud import knowledgebase as crud_knowledgebase
from ..core.database import get_db
from ..core.config import settings
from sqlalchemy.orm import Session
import tempfile
import os
import asyncio
import time
from qdrant_client.http.exceptions import ResponseHandlingException, UnexpectedResponse
import logging

logger = logging.getLogger(__name__)
 
class IndexService:
    def __init__(self):
        self.minio_client = get_minio_client()
        self.qdrant_client = get_qdrant_client()
        self.async_qdrant_client = get_async_qdrant_client()
        self.db = next(get_db())

    async def create_index(self, knowledgebase_id: int):
        db_knowledgebase = crud_knowledgebase.get_knowledgebase(self.db, knowledgebase_id)
        if not db_knowledgebase:
            raise ValueError(f"Knowledgebase with id {knowledgebase_id} not found")

        # Create a new index entry in the database
        db_index = crud_index.create_index(self.db, {"knowledgebase_id": knowledgebase_id})
        collection_name = f"kb_{knowledgebase_id}_index_{db_index.id}"
        db_index = crud_index.update_index(self.db, db_index, {"qdrant_collection_name": collection_name})

        try:
            # Delete collection if it exists
            if await self.async_qdrant_client.collection_exists(collection_name):
                await self.async_qdrant_client.delete_collection(collection_name)

            # Create vector store with hybrid indexing
            vector_store = QdrantVectorStore(
                collection_name,
                client=self.qdrant_client,
                aclient=self.async_qdrant_client,
                enable_hybrid=True,
                batch_size=20,
                fastembed_sparse_model="Qdrant/bm42-all-minilm-l6-v2-attentions"
            )

            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            Settings.chunk_size = 512
            Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

            documents = await self._load_documents(db_knowledgebase.documents)

            # Implement retry logic with exponential backoff
            max_retries = 5
            base_delay = 1
            for attempt in range(max_retries):
                try:
                    index = VectorStoreIndex.from_documents(
                        documents,
                        storage_context=storage_context,
                    )
                    break
                except (ResponseHandlingException, UnexpectedResponse) as e:
                    if attempt == max_retries - 1:
                        logger.error(f"Failed to create index after {max_retries} attempts: {str(e)}")
                        raise
                    delay = base_delay * (2 ** attempt)
                    logger.warning(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)

            # Update index size and set is_indexed to True in the database
            new_size = len(documents)
            crud_index.update_index(self.db, db_index, {"index_size": new_size})
            crud_knowledgebase.update_knowledgebase(self.db, db_knowledgebase, {"is_indexed": True})

            return index
        except Exception as e:
            logger.error(f"Error creating index: {str(e)}")
            # Delete the index entry if creation failed
            crud_index.delete_index(self.db, db_index.id)
            raise

    async def _load_documents(self, db_documents):
        documents = []
        with tempfile.TemporaryDirectory() as temp_dir:
            for db_document in db_documents:
                try:
                    file_obj = self.minio_client.get_object(settings.MINIO_BUCKET_NAME,
                        db_document.file_path)
                    file_path = os.path.join(temp_dir, db_document.filename)
                    with open(file_path, "wb") as f:
                        for d in file_obj.stream(32*1024):
                            f.write(d)

                    documents.extend(SimpleDirectoryReader(temp_dir).load_data())
                except Exception as e:
                    print(f"Error loading document {db_document.id}: {str(e)}")

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

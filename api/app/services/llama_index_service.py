from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from ..core.qdrant_client import get_qdrant_client
from ..core.minio_client import get_minio_client
from ..core.config import settings
from ..crud.document import get_document
from ..core.database import get_db
import tempfile
import os

def index_documents(knowledgebase_id: int, document_ids: list[int]):
    minio_client = get_minio_client()
    qdrant_client = get_qdrant_client()
    db = next(get_db())

    with tempfile.TemporaryDirectory() as temp_dir:
        for doc_id in document_ids:
            try:
                # Get the document from the database
                db_document = get_document(db, doc_id)
                if not db_document:
                    print(f"Document with id {doc_id} not found in the database.")
                    continue

                # Fetch document from MinIO using the stored file_path
                file_obj = minio_client.get_object(settings.MINIO_BUCKET_NAME, db_document.file_path)
                file_path = os.path.join(temp_dir, db_document.filename)
                with open(file_path, "wb") as f:
                    for d in file_obj.stream(32*1024):
                        f.write(d)
            except Exception as e:
                print(f"Error fetching document {doc_id}: {str(e)}")
                continue  # Skip this document and continue with the next

        # Load documents
        documents = SimpleDirectoryReader(temp_dir).load_data()

        if not documents:
            print("No documents were successfully loaded.")
            return None

        # Create Qdrant vector store
        vector_store = QdrantVectorStore(client=qdrant_client, collection_name=f"knowledgebase_{knowledgebase_id}")
        
        # Use HuggingFace embeddings
        # embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
        embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
        
        Settings.embed_model = embed_model

        llm = Ollama(model="llama3.1", base_url="http://ollama:11434", request_timeout=300)
        
        Settings.llm = llm

        # Create index
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(
            documents, 
            storage_context=storage_context
        )
        

    return index

def query_knowledgebase(knowledgebase_id: int, query: str):
    qdrant_client = get_qdrant_client()
    vector_store = QdrantVectorStore(client=qdrant_client, collection_name=f"knowledgebase_{knowledgebase_id}")
    
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    
    Settings.embed_model = embed_model

    llm = Ollama(model="llama3.1", base_url="http://ollama:11434", request_timeout=300)
    
    Settings.llm = llm

    index = VectorStoreIndex.from_vector_store(vector_store)
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return response
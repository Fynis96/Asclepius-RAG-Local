from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.llms.ollama import Ollama
from llama_index.core import (
    Settings, 
    VectorStoreIndex, 
    ChatPromptTemplate,
    StorageContext,
    load_index_from_storage
    )
from llama_index.core.llms import ChatMessage
from llama_index.core.chat_engine import CondensePlusContextChatEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata, BaseTool, FunctionTool
from llama_index.core.agent import ReActAgent
from llama_index.core.query_engine import RouterQueryEngine, SubQuestionQueryEngine, CitationQueryEngine
from ..core.qdrant_client import get_qdrant_client, get_async_qdrant_client
from ..core.database import get_db
from ..core.config import settings
from ..core.logger import get_logger

from ..crud import chat as crud_chat
from ..crud import index as crud_index
from ..crud import knowledgebase as crud_knowledgebase
from sqlalchemy.orm import Session

logger = get_logger(__name__)

class ChatService:
    def __init__(self):
        self.qdrant_client = get_qdrant_client()
        self.async_qdrant_client = get_async_qdrant_client()
        self.db = next(get_db())

    async def create_chatbot(self, user_id: int, name: str, model: str, temperature: float, chatmode: str, engine_type: str, index_id: int = None):
        try:
            chatbot_data = {
                "user_id": user_id,
                "name": name,
                "model": model,
                "temperature": temperature,
                "chatmode": chatmode,
                "engine_type": engine_type,
                "index": index_id
            }
            
            db_chatbot = crud_chat.create_chatbot(self.db, chatbot_data)
            
            if index_id:
                # Verify that the index exists
                db_index = crud_index.get_index(self.db, index_id)
                if not db_index:
                    raise ValueError(f"Index with id {index_id} not found")
            
            return db_chatbot
        except Exception as e:
            logger.error(f"Error creating chatbot: {str(e)}")
            raise

chat_service = ChatService()
        
# Hybrid Search functionality using llama-index for reference.

# documents = SimpleDirectoryReader(input_files=[file_path]).load_data()

# client = QdrantClient(host="localhost", port=6333)
# aclient = AsyncQdrantClient(host="localhost", port=6333)

# collection_name = "testing_out"

# # delete collection if it exists
# if client.collection_exists(collection_name):
#     client.delete_collection(collection_name)

# # create our vector store with hybrid indexing enabled
# # batch_size controls how many nodes are encoded with sparse vectors at once
# vector_store = QdrantVectorStore(
#     collection_name,
#     client=client,
#     aclient=aclient,
#     enable_hybrid=True,
#     batch_size=20,
#     fastembed_sparse_model="Qdrant/bm42-all-minilm-l6-v2-attentions"
# )

# storage_context = StorageContext.from_defaults(vector_store=vector_store)
# Settings.chunk_size = 512

# index = VectorStoreIndex.from_documents(
#     documents,
#     storage_context=storage_context,
# )

# chat_engine = index.as_chat_engine(
#     chat_mode="condense_plus_context",
#     llm=llm
# )

# response = chat_engine.chat("What was the largest dollar amount discussed and why?")
# print(str(response))

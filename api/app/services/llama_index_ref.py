import logging
import sys
import json
import os
from typing import Sequence, List

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, AsyncQdrantClient

from llama_index.core import (
    Settings, 
    VectorStoreIndex, 
    SummaryIndex, 
    SimpleDirectoryReader, 
    ChatPromptTemplate,
    StorageContext,
    load_index_from_storage
    )
from llama_index.core.tools import QueryEngineTool, ToolMetadata, BaseTool, FunctionTool
from llama_index.core.agent import ReActAgent
from llama_index.core.query_engine import RouterQueryEngine, SubQuestionQueryEngine, CitationQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.prompts import PromptTemplate
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine import CondensePlusContextChatEngine
from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler
from pydantic import BaseModel
from llama_index.core.llms import ChatMessage


llama_debug = LlamaDebugHandler(print_trace_on_end=True)
callback_manager = CallbackManager([llama_debug])

Settings.callback_manager = callback_manager

llm = Ollama(model="llama3.1", base_url="http://localhost:11434", request_timeout=300, temperature=0.2)
# embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Settings.llm = llm
# Settings.embed_model = embed_model

# docs = SimpleDirectoryReader(input_dir="C:\\source\\Learning\\llama\\data").load_data()
# docs = SimpleDirectoryReader(input_files=["C:\\source\\Learning\\llama\\paul_graham_essay.txt"]).load_data()

# folder_path = "C:\\source\\Learning\\llama\\data"
# file_path = "C:\\source\\Learning\\llama\\paul_graham_essay.txt"

# docs = SimpleDirectoryReader(folder_path).load_data()

# #Basic RAG (Vector Search):
# index = VectorStoreIndex.from_documents(docs)
# query_engine = index.as_query_engine(similarity_top_k=3)
# query_engine.
# response = query_engine.query("What is the largest dollar amount discussed and why?")
# print(str(response))

#Advanced RAG (Routing, Sub-Questions)
# vector_tool = QueryEngineTool(
#     index.as_query_engine(),
#     metadata=ToolMetadata(
#         name="vector_search",
#         description="Useful for searching for specific facts.",
#     ),
# )

# summary_tool = QueryEngineTool(
#     index.as_query_engine(response_mode="tree_summarize"),
#     metadata=ToolMetadata(
#         name="summary",
#         description="Useful for summarizing an entire document.",
#     ),
# )

# query_engine = RouterQueryEngine.from_defaults(
#     [vector_tool, summary_tool], select_multi=False, verbose=True
# )

# vector_query_engine = VectorStoreIndex.from_documents(docs, use_async=True).as_query_engine()
# response = query_engine.query(
#     "Summarize the Document as best and terse as possible."
# )
# print(response)

# response = query_engine.query(
#     "What is the largest dollar amount discussed and why?"
# )
# print(response)

#Sub-Questions

# query_engine_tools = [
#     QueryEngineTool(
#         query_engine=vector_query_engine,
#         metadata=ToolMetadata(
#             name="pg_essay",
#             description="Paul Graham essay on What I Worked On",
#         ),
#     ),
# ]

# query_engine = SubQuestionQueryEngine.from_defaults(
#     query_engine_tools=query_engine_tools, verbose=True, use_async=True
# )

# response = query_engine.query("What is one of the biggest arguments being made by the author?")

# print(response)

# from llama_index.core.callbacks import CBEventType, EventPayload

# for i, (start_event, end_event) in enumerate(
#     llama_debug.get_event_pairs(CBEventType.SUB_QUESTION)
# ):
#     qa_pair = end_event.payload[EventPayload.SUB_QUESTION]
#     print("Sub Question " + str(i) + ": " + qa_pair.sub_q.sub_question.strip())
#     print("Answer: " + qa_pair.answer.strip())
#     print("====================================")

#Structured Data Extraction:
# class Restaurant(BaseModel):
#     """ A Restaurant with name, city, and cuisine."""
#     name: str
#     city: str
#     cuisine: str

# prompt_tmpl = PromptTemplate(
#     "Generate restaurant in a given city {city_name}"
# )

# restaurant_obj = llm.structured_predict(
#     Restaurant, prompt_tmpl, city_name="Miami"
# )
# print(restaurant_obj)

# Adding chat history to RAG (Chat Engine)
# memory = ChatMemoryBuffer.from_defaults(token_limit=3900)

# chat_engine = CondensePlusContextChatEngine.from_defaults(
#     index.as_retriever(),
#     memory=memory,
#     llm=llm,
#     context_prompt=(
#         "You are a chatbot, able to have normal interactions, as well as talk"
#         " about the contents of the document."
#         "Here are the relevant documents for the context:\n"
#         "{context_str}"
#         "\nInstruction: Use the previous chat history, or the context above, to to interact and help the user."
#     ),
#     verbose=True
# )

# response = chat_engine.chat(
#     "Summarize the document in a few sentences."
# )
# print(response)

# response = chat_engine.chat("Are you certain that's a fine summary?")
# print(response)

#ReACT agent

# def multiply(a: int, b: int) -> int:
#     """Multiple two integers and returns the result integer"""
#     return a * b


# def add(a: int, b: int) -> int:
#     """Add two integers and returns the result integer"""
#     return a + b


# def subtract(a: int, b: int) -> int:
#     """Subtract two integers and returns the result integer"""
#     return a - b


# def divide(a: int, b: int) -> int:
#     """Divides two integers and returns the result integer"""
#     return a / b


# multiply_tool = FunctionTool.from_defaults(fn=multiply)
# add_tool = FunctionTool.from_defaults(fn=add)
# subtract_tool = FunctionTool.from_defaults(fn=subtract)
# divide_tool = FunctionTool.from_defaults(fn=divide)

# json_llm = Ollama(model="llama3.1", base_url="http://localhost:11434", request_timeout=300, temperature=0.2, json_mode=True)

# agent = ReActAgent.from_tools(
#     [multiply_tool, add_tool, subtract_tool, divide_tool],
#     llm=llm,
#     verbose=True,
# )


# response = agent.chat("What is (121 + 2) * 5?")
# print(str(response))

# ReAct Agent with RAG queryengine tools

# docs = SimpleDirectoryReader(input_dir="C:\\source\\Learning\\llama\\data").load_data()
# docs2 = SimpleDirectoryReader(input_files=["C:\\source\\Learning\\llama\\paul_graham_essay.txt"]).load_data()

# index = VectorStoreIndex.from_documents(docs)
# index2 = VectorStoreIndex.from_documents(docs2)

# doc_tool = QueryEngineTool(
#     index.as_query_engine(),
#     metadata=ToolMetadata(
#         name="bigdoc_search",
#         description="Useful for searching for specific facts.",
#     ),
# )

# doc2_tool = QueryEngineTool(
#     index2.as_query_engine(),
#     metadata=ToolMetadata(
#         name="pg_essay",
#         description="Paul Graham essay on What I Worked On",
#     ),
# )

# query_engine_tools = [doc_tool, doc2_tool]

# agent = ReActAgent.from_tools(
#     query_engine_tools,
#     llm=llm,
#     verbose=True,
# )

# response = agent.chat("Tell me about the similarities in the bigdoc, and the pg_essay.")
# print(str(response))


# CitationQueryEngine
# if not os.path.exists("./citation"):
#     # documents = SimpleDirectoryReader(input_files=["C:\\source\\Learning\\llama\\paul_graham_essay.txt"]).load_data()
#     documents = SimpleDirectoryReader(input_dir="C:\\source\\Learning\\llama\\data").load_data()
    
#     index = VectorStoreIndex.from_documents(documents)
#     index.storage_context.persist(persist_dir="./citation")
# else:
#     index = load_index_from_storage(
#         StorageContext.from_defaults(persist_dir="./citation")
#     )
    
# documents = SimpleDirectoryReader(input_dir="C:\\source\\Learning\\llama\\data").load_data()

# summary_index = SummaryIndex.from_documents(documents)

# query_engine = CitationQueryEngine.from_args(
#     summary_index,
#     similarity_top_k=3,
#     citation_chunk_size=1024
# )

# response = query_engine.query("What is the largest dollar amount discussed and why?")
# print(response)

# print(len(response.source_nodes))
# print("\n\n\n")
# print(response.source_nodes[0].node.get_text())


# Hybrid Search

# documents = SimpleDirectoryReader(folder_path).load_data()
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

# response = chat_engine.chat("Summarize the document in a few sentences.")
# print(str(response))

# response = chat_engine.chat("What was one of the most devestating impacts noted in the document?")
# print(str(response))

#Json Modes



#Random

# response = llm.stream_complete("Hello!")
# for r in response:
#     print(r.delta, end="")


# messages = [
#     ChatMessage(role="user", content="What is your name"),
# ]

# resp = llm.stream_chat(messages)
# for r in resp:
#     print(r.delta, end="")
    
# messages = [
#     ChatMessage(role="user", content="Hello!"),
#     ChatMessage(role="system", content="Hello! How can I help you today?"),
#     ChatMessage(role="user", content="What is your name?"),
#     ChatMessage(role="system", content="My name is Llama!"),
#     ChatMessage(role="user", content="What was my greeting?")
# ]
# resp = llm.stream_chat(messages)
# response_content = ""
# for r in resp:
#     response_content += r.delta
#     print(r.delta, end="")
    
    
# message = ChatMessage(role="system", content=response_content)
# messages.append(message)

# message = ChatMessage(role="user", content="What is your name?")
# messages.append(message)
# resp = llm.stream_chat(messages)

# for r in resp:
#     print(r.delta, end="")
    
# message = ChatMessage(role="user", content="How many times have we seemed to go back and forth?")

# messages.append(message)
# resp = llm.stream_chat(messages)
# for r in resp:
#     print(r.delta, end="")
    
    

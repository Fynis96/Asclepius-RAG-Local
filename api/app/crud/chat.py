from sqlalchemy.orm import Session
from ..models.chat import Chatbot, Chat
# from ..schemas.chat import 
from ..core.config import settings
import uuid

def create_chatbot():
    # create a chatbot with default values
    pass

def delete_chatbot():
    pass

def get_chatbot():
    pass

def get_chatbots():
    pass

def update_chatbot():
    pass

def create_chat():
    # load up values needed to create/query llama index index.as_qeury_engine or index.as_chat_engine
    pass

def delete_chat():
    pass

def get_chat():
    pass

def get_chats():
    pass

def update_chat():
    # using the chatbot_id, message content, index_id, and user_id, update the chat, return updated chat history with response
    # how to provide streaming chat in this way? Maybe just let the front end provide that magic heh
    # this will probably branch a bit
    # if chat_engine uses history, loading the history into the chat engine before sending message
    pass


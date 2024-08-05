from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from ...core.database import get_db
from ...schemas.user import User
from ..deps import get_current_user

def create_chatbot():
    pass

def delete_chatbot():
    pass

def get_chatbot():
    # if index
    # if not query engine
        # load chat history to chatbot
    pass

def get_chatbots():
    pass

def update_chatbot():
    pass

def create_chat():
    pass

def delete_chat():
    pass

def get_chat():
    pass

def get_chats():
    pass

def update_chat():
    # update chat history
    pass

def clear_chat_history():
    pass
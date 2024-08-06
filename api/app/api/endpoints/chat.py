from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_current_user, get_db
from ...schemas.user import User
from ..deps import get_current_user
from ...schemas.chat import ChatbotCreate, ChatbotResponse
from ...services.chat_service import chat_service

router = APIRouter()

@router.post("/chatbots", response_model=ChatbotResponse)
async def create_chatbot(
    chatbot: ChatbotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        db_chatbot = await chat_service.create_chatbot(
            user_id=current_user.id,
            name=chatbot.name,
            model=chatbot.model,
            temperature=chatbot.temperature,
            chatmode=chatbot.chatmode,
            engine_type=chatbot.engine_type,
            index_id=chatbot.index
        )
        return db_chatbot
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

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
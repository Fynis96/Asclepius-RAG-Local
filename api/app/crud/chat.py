from sqlalchemy.orm import Session
from ..models.chat import Chatbot
from ..schemas.chat import ChatbotCreate
from ..core.config import settings
import uuid

def create_chatbot(db: Session, chatbot: ChatbotCreate):
    db_chatbot = Chatbot(**chatbot.dict())
    db.add(db_chatbot)
    db.commit()
    db.refresh(db_chatbot)
    return db_chatbot

def get_chatbot(db: Session, chatbot_id: int):
    return db.query(Chatbot).filter(Chatbot.id == chatbot_id).first()

def get_chatbots_by_user(db: Session, user_id: int):
    return db.query(Chatbot).filter(Chatbot.user_id == user_id).all()

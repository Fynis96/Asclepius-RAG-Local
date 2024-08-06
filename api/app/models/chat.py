from ..core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from .timestamp import TimestampMixin

class Chatbot(Base, TimestampMixin):
    __tablename__ = "chatbots"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    model = Column(String)
    temperature = Column(Float)
    chatmode = Column(String)
    engine_type = Column(String)
    index = Column(Integer, nullable=True)
    
    user = relationship("User", back_populates="chatbots")
    chats = relationship("Chat", back_populates="chatbot")
    

class Chat(Base, TimestampMixin):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    chatbot_id = Column(Integer, ForeignKey("chatbots.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    chatbot = relationship("Chatbot", back_populates="chats")
    user = relationship("User", back_populates="chats")
    messages = relationship("Message", back_populates="chat")

class Message(Base, TimestampMixin):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    role = Column(String)
    message_metadata = Column(JSON)
    
    chat = relationship("Chat", back_populates="messages")
    user = relationship("User", back_populates="messages")


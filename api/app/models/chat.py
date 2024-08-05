from ..core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .timestamp import TimestampMixin

class Chatbot(Base, TimestampMixin):
    __tablename__ = "chatbots"
    id = Column(Integer, primary_key=True, index=True)
    # name = Column(String, index=True)
    # user_id = Column(Integer, ForeignKey("users.id"))
    # model
    # temperature
    # chatmode
    # engine_type (query or chat)
        # query_engine doesn't have chat history
    # index (nullable)
    # chats = relationship("Chat", back_populates="chatbot")
    

class Chat(Base, TimestampMixin):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    # chatbot_id = Column(Integer, ForeignKey("chatbots.id"))
    # user_id = Column(Integer, ForeignKey("users.id"))
    # messages
    

class Message(Base, TimestampMixin):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    # chat_id = Column(Integer, ForeignKey("chats.id"))
    # user_id = Column(Integer, ForeignKey("users.id"))
    # message (user or bot)
    # role
    # citations/metadata


from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from .timestamp import TimestampMixin
from ..core.database import Base

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    refresh_token = Column(String, nullable=True)

    knowledgebases = relationship("Knowledgebase", back_populates="user")
    chatbots = relationship("Chatbot", back_populates="user")
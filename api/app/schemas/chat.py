from pydantic import BaseModel
from typing import List

class ChatbotCreate(BaseModel):
    name: str
    model: str
    temperature: float
    chatmode: str
    engine_type: str
    index_id: int

class ChatbotResponse(ChatbotCreate):
    id: int
    user_id: int

class ChatCreate(BaseModel):
    chatbot_id: int

class ChatResponse(ChatCreate):
    id: int
    user_id: int

class MessageCreate(BaseModel):
    content: str
    role: str

class MessageResponse(MessageCreate):
    id: int
    chat_id: int
    user_id: int

class ChatHistoryResponse(BaseModel):
    messages: List[MessageResponse]


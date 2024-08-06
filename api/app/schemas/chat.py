from pydantic import BaseModel
from typing import List

class ChatbotBase(BaseModel):
    name: str
    model: str
    temperature: float
    chatmode: str
    engine_type: str
    index: Optional[int] = None

class ChatbotCreate(ChatbotBase):
    pass

class ChatbotResponse(ChatbotBase):
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




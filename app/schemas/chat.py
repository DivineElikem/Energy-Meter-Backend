from pydantic import BaseModel

class ChatQuery(BaseModel):
    question: str
    session_id: str

class ChatResponse(BaseModel):
    answer: str

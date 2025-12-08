from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.chat_service import ask_chatbot
from app.schemas.chat import ChatQuery, ChatResponse

router = APIRouter()

@router.post("/query", response_model=ChatResponse)
def query_chatbot(
    query: ChatQuery,
    db: Session = Depends(get_db)
):
    answer = ask_chatbot(query.question, query.session_id, db)
    return {"answer": answer}

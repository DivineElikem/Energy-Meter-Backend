from typing import Dict, List
import os
from groq import Groq
from sqlalchemy.orm import Session
from app.config import settings
from app.db import crud
from datetime import date, timedelta

# Initialize Groq client
# Ensure GROQ_API_KEY is set in .env
client = Groq(api_key=settings.GROQ_API_KEY)

# In-memory store for chat sessions
# Format: {session_id: [{"role": "user", "content": "..."}, ...]}
chat_sessions: Dict[str, List[Dict]] = {}

def get_context(db: Session):
    """Fetches relevant context from the database for the chatbot."""
    # For simplicity, let's fetch yesterday's summary and today's summary
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    today_stats = crud.get_daily_usage(db, today)
    yesterday_stats = crud.get_daily_usage(db, yesterday)
    
    context = f"Today's Date: {today}\n"
    
    context += "Today's Usage:\n"
    for device in today_stats:
        context += f"- {device['device']}: {device['total_energy']} kWh\n"
        
    context += "Yesterday's Usage:\n"
    for device in yesterday_stats:
        context += f"- {device['device']}: {device['total_energy']} kWh\n"
        
    return context

def ask_chatbot(question: str, session_id: str, db: Session):
    """Queries the Groq LLaMA-3 model with context and history."""
    
    if not settings.GROQ_API_KEY:
        return "I'm sorry, but the Groq API key is not configured."

    context = get_context(db)
    
    system_prompt = f"""You are "Energy Boss", a smart, witty, and slightly authoritative energy meter assistant.
    Your goal is to help users understand their energy consumption and save money.
    
    You have access to the following energy usage data:
    {context}
    
    Guidelines:
    1. **Personality**: Be confident, helpful, and a bit playful. Use emojis occasionally ⚡💡.
    2. **Data Usage**: Always base your answers on the provided data. If you don't know, admit it but suggest checking the dashboard.
    3. **Follow-ups**: Remember the conversation context.
    4. **Alerts**: If you see high usage (e.g., > 2.0 kWh for a socket, or > 0.5 kWh for a bulb), warn the user playfully (e.g., "Whoa, someone's power hungry!").
    5. **Phrasing**: Never say "based on the data provided" or "according to the data". You ARE the system, so you just know this information directly.
    
    Answer the user's question concisely.
    """
    
    # Initialize session if not exists
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    
    # Add user message to history
    chat_sessions[session_id].append({"role": "user", "content": question})
    
    # Prepare messages for API call
    # We include the system prompt + history
    messages = [{"role": "system", "content": system_prompt}] + chat_sessions[session_id]
    
    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.1-8b-instant",
        )
        answer = chat_completion.choices[0].message.content
        
        # Add assistant response to history
        chat_sessions[session_id].append({"role": "assistant", "content": answer})
        
        return answer
    except Exception as e:
        print(f"Groq API Error: {e}")
        return "I'm sorry, I'm having trouble connecting to my brain right now. 🤯"

# api/app/routes/chat.py
from fastapi import APIRouter
from app.services.llm_service import chat_llm

router = APIRouter()

chat_history = []  # lưu tại RAM (nếu muốn lưu DB thì tách riêng)

@router.post("/chat")
async def chat_endpoint(payload: dict):
    user_message = payload.get("message", "")
    response = chat_llm(user_message, chat_history)
    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role": "assistant", "content": response})
    return {"response": response, "history": chat_history}

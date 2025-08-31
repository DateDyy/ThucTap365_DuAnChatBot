from fastapi import APIRouter
from api.app.services.llm_service import chat_llm

router = APIRouter()

chat_history = []

@router.post("/chat")
async def chat_endpoint(payload: dict):
    user_message = payload.get("message") or payload.get("user_message", "")
    history = payload.get("history", [])

    response = chat_llm(user_message, history)
    return {"response": response, "history": history}

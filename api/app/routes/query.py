from fastapi import APIRouter
from app.services.llm_service import query_llm

router = APIRouter()

@router.post("/query")
async def query_endpoint(payload: dict):
    question = payload.get("question", "")
    answer = query_llm(question)
    return {"question": question, "answer": answer}

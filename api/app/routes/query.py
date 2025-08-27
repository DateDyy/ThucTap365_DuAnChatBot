from fastapi import APIRouter
from pydantic import BaseModel
from api.app.services.llm_service import query_llm

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
async def query_endpoint(payload: QueryRequest):
    answer = query_llm(payload.question)
    return {"question": payload.question, "answer": answer}

# api/app/routes/update.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.vector_service import add_document

router = APIRouter()

class UpdateRequest(BaseModel):
    text: str
    metadata: dict = {}

@router.post("/update")
async def update_endpoint(req: UpdateRequest):
    add_document(req.text, req.metadata)
    return {"status": "success", "message": "Document added to FAISS index"}

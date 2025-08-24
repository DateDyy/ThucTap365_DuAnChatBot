from langchain.prompts import PromptTemplate

RAG_TEMPLATE = """Bạn là chatbot AI dành cho sinh viên và có nhiệm vụ giúp đỡ sinh viên trong việc học môn lập trình web.
Ngữ cảnh dưới đây có thể giúp bạn trả lời câu hỏi:
{context}

Câu hỏi: {question}

Hãy trả lời ngắn gọn, chính xác, trích dẫn thông tin nếu có.
"""

rag_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=RAG_TEMPLATE
)

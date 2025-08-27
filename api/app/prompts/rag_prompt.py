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

CHAT_TEMPLATE = """Bạn là chatbot AI hỗ trợ sinh viên trong việc học lập trình web.
Người dùng vừa hỏi:
{question}

Hãy trả lời một cách tự nhiên, ngắn gọn và dễ hiểu, không cần trích dẫn.
"""

chat_prompt = PromptTemplate(
    input_variables=["question"],
    template=CHAT_TEMPLATE
)

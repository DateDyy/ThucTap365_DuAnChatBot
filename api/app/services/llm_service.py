import os
from dotenv import load_dotenv
from api.app.services.vector_service import db
from api.app.prompts.rag_prompt import rag_prompt, chat_prompt
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

# ====== Load token từ .env ======
load_dotenv()
hf_token = os.getenv("HF_TOKEN")

if not hf_token:
    raise ValueError("HF_TOKEN chưa được cấu hình trong file .env")

# ====== Tạo LLM gốc ======
base_llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Meta-Llama-3-8B-Instruct",   # ✅ model có hỗ trợ chat
    task="conversational",                           # phải là conversational
    huggingfacehub_api_token=hf_token,
    temperature=0.7,
    max_new_tokens=512
)

# ====== Bọc thành ChatModel ======
llm = ChatHuggingFace(llm=base_llm)

# ====== Hàm an toàn gọi FAISS ======
def safe_similarity_search(query: str, k: int = 3):
    try:
        return db.similarity_search(query, k=k)
    except KeyError as e:
        print(f"⚠️ Lỗi FAISS index không đồng bộ với metadata: {e}")
        return []
    except Exception as e:
        print(f"⚠️ Lỗi khác khi tìm kiếm FAISS: {e}")
        return []

# ====== Query RAG ======
def query_llm(user_query: str, k: int = 3):
    docs = safe_similarity_search(user_query, k=k)
    if not docs:
        return "Dữ liệu tìm kiếm chưa đồng bộ hoặc không khả dụng. Hãy rebuild lại vector store."

    context = "\n\n".join([d.page_content for d in docs])
    prompt = rag_prompt.format(context=context, question=user_query)

    return llm.invoke([
        {"role": "system", "content": "Bạn là một trợ lý AI thông minh."},
        {"role": "user", "content": prompt}
    ])

# ====== Chat có lịch sử ======
def chat_llm(user_message: str, history: list, k: int = 3):
    docs = safe_similarity_search(user_message, k=k)
    if not docs:
        return "Dữ liệu tìm kiếm chưa đồng bộ hoặc không khả dụng. Hãy rebuild lại vector store."

    context = "\n\n".join([d.page_content for d in docs])
    history_text = "\n".join([f"{h['role']}: {h['content']}" for h in history])
    prompt = chat_prompt.format(history=history_text, context=context, question=user_message)

    return llm.invoke([
        {"role": "system", "content": "Bạn là một trợ lý AI hỗ trợ hội thoại."},
        {"role": "user", "content": prompt}
    ])

def add_document(text: str, metadata: dict):
    # Logic để thêm tài liệu vào FAISS index
    print(f"Adding document: {text} with metadata: {metadata}")
    # Thêm logic xử lý FAISS hoặc lưu trữ tại đây

import os
from dotenv import load_dotenv
from app.services.vector_service import db
from app.prompts.rag_prompt import rag_prompt, chat_prompt
from langchain_community.llms import HuggingFaceHub  

# ====== Load token từ .env ======
load_dotenv()  
hf_token = os.getenv("HF_TOKEN")

if not hf_token:
    raise ValueError("HF_TOKEN chưa được cấu hình trong file .env")

# ====== Cấu hình Hugging Face Hub ======
llm = HuggingFaceHub(
    repo_id="HuggingFaceH4/zephyr-7b-beta",   # model miễn phí
    huggingfacehub_api_token=hf_token,        # truyền token từ .env
    model_kwargs={
        "temperature": 0.7,
        "max_new_tokens": 512
    }
)

# ====== Query RAG ======
def query_llm(user_query: str, k: int = 3):
    docs = db.similarity_search(user_query, k=k)
    context = "\n\n".join([d.page_content for d in docs])
    prompt = rag_prompt.format(context=context, question=user_query)
    return llm.invoke(prompt)

# ====== Chat có lịch sử ======
def chat_llm(user_message: str, history: list, k: int = 3):
    docs = db.similarity_search(user_message, k=k)
    context = "\n\n".join([d.page_content for d in docs])
    history_text = "\n".join([f"{h['role']}: {h['content']}" for h in history])
    prompt = chat_prompt.format(history=history_text, context=context, question=user_message)
    return llm.invoke(prompt)

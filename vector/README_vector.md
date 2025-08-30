# Thư mục `vector` - Xử lý và quản lý FAISS Vector Store

Thư mục `vector` chứa mã nguồn và dữ liệu liên quan đến việc xây dựng, kiểm tra, và quản lý FAISS Vector Store, phục vụ cho hệ thống Chatbot RAG.

---

## Cấu trúc thư mục

```
vector/
├── faiss_store/                # Thư mục chứa FAISS Vector Store đã xây dựng
│   ├── index.faiss             # File FAISS index lưu trữ vector
│   ├── index.pkl               # File pickle lưu metadata của vector
├── src/data/                   # Thư mục chứa các script xử lý vector
│   ├── build_vector_store.py   # Script xây dựng FAISS Vector Store từ dữ liệu
│   ├── check_vector_entry.py   # Script kiểm tra các entry trong FAISS Vector Store
├── README_vector.md            # Tài liệu hướng dẫn sử dụng thư mục vector
```

---

## Chức năng các file và thư mục

### **1. faiss_store/**
- **Mục đích**: Lưu trữ FAISS index và metadata.
- **Các file**:
  - `index.faiss`: File FAISS index chứa các vector đã được xây dựng.
  - `index.pkl`: File pickle chứa metadata liên quan đến các vector (ví dụ: thông tin ngữ cảnh, nhãn).

---

### **2. src/data/build_vector_store.py**
- **Mục đích**: Xây dựng FAISS Vector Store từ dữ liệu đầu vào.
- **Chức năng**:
  - Đọc dữ liệu từ các file JSON hoặc TXT.
  - Tạo vector embedding từ dữ liệu.
  - Lưu vector và metadata vào FAISS index.
- **Cách sử dụng**:
  - Chạy lệnh:
    ```bash
    python src/data/build_vector_store.py
    ```
  - Dữ liệu đầu vào cần được chuẩn bị trước (ví dụ: file JSON chứa văn bản và metadata).
  - FAISS index sẽ được lưu vào thư mục `faiss_store`.

---

### **3. src/data/check_vector_entry.py**
- **Mục đích**: Kiểm tra các entry trong FAISS Vector Store.
- **Chức năng**:
  - Đọc FAISS index và metadata từ thư mục `faiss_store`.
  - Kiểm tra thông tin từng vector (ví dụ: ngữ cảnh, nhãn).
  - Hiển thị thông tin để xác nhận dữ liệu đã được lưu đúng.
- **Cách sử dụng**:
  - Chạy lệnh:
    ```bash
    python src/data/check_vector_entry.py
    ```
  - Script sẽ hiển thị thông tin chi tiết về các vector trong FAISS index.

---

### **4. Tích hợp mô hình `meta-llama/Meta-Llama-3-8B-Instruct`**
- **Mục đích**: Sử dụng mô hình ngôn ngữ lớn (LLM) để tóm tắt dữ liệu hoặc sinh câu trả lời dựa trên ngữ cảnh từ FAISS Vector Store.
- **Công nghệ**:
  - **Hugging Face Endpoint**: Tích hợp mô hình LLM từ Hugging Face thông qua API.
  - **Mô hình `meta-llama/Meta-Llama-3-8B-Instruct`**:
    - Mô hình ngôn ngữ lớn với 8 tỷ tham số, tối ưu hóa cho các tác vụ hội thoại và hướng dẫn.
    - Được sử dụng để sinh văn bản tự nhiên và tóm tắt thông tin từ dữ liệu.
- **Chức năng**:
  - **Tóm tắt dữ liệu**:
    - Trích xuất ngữ cảnh từ FAISS Vector Store.
    - Gửi ngữ cảnh đến mô hình LLM để tạo tóm tắt.
  - **Sinh câu trả lời**:
    - Kết hợp ngữ cảnh từ FAISS Vector Store với câu hỏi của người dùng.
    - Sử dụng mô hình LLM để sinh câu trả lời tự nhiên và chính xác.
- **Ví dụ sử dụng**:
  - Tóm tắt dữ liệu:
    ```python
    def summarize_context(context: str):
        response = llm.generate(context)
        return response
    ```
  - Sinh câu trả lời:
    ```python
    def generate_answer(question: str, context: str):
        prompt = f"Câu hỏi: {question}\nNgữ cảnh: {context}\nHãy trả lời ngắn gọn và chính xác."
        response = llm.generate(prompt)
        return response
    ```

---

## Hướng dẫn sử dụng

### **1. Cài đặt các thư viện cần thiết**
- Tạo môi trường ảo:
  ```bash
  python -m venv venv
  ```
- Kích hoạt môi trường ảo:
  - **Windows**:
    ```bash
    venv\Scripts\activate
    ```
  - **Linux/macOS**:
    ```bash
    source venv/bin/activate
    ```
- Cài đặt các thư viện:
  ```bash
  pip install faiss-cpu numpy pandas langchain langchain-huggingface
  ```

---

### **2. Xây dựng FAISS Vector Store**
- Chuẩn bị dữ liệu đầu vào (file JSON hoặc TXT chứa văn bản và metadata).
- Chạy lệnh:
  ```bash
  python src/data/build_vector_store.py
  ```
- FAISS index sẽ được lưu vào thư mục `faiss_store`.

---

### **3. Kiểm tra FAISS Vector Store**
- Chạy lệnh:
  ```bash
  python src/data/check_vector_entry.py
  ```
- Kiểm tra thông tin từng vector để xác nhận dữ liệu đã được lưu đúng.

---

### **4. Tóm tắt và sinh câu trả lời**
- Sử dụng mô hình `meta-llama/Meta-Llama-3-8B-Instruct` để tóm tắt hoặc sinh câu trả lời:
  - Tóm tắt dữ liệu:
    ```python
    context = "Đây là ngữ cảnh cần tóm tắt."
    summary = summarize_context(context)
    print(summary)
    ```
  - Sinh câu trả lời:
    ```python
    question = "Làm thế nào để sử dụng HTML?"
    context = "HTML là ngôn ngữ đánh dấu được sử dụng để tạo trang web."
    answer = generate_answer(question, context)
    print(answer)
    ```

---

### **5. Lưu ý**
- Đảm bảo token API của Hugging Face được cấu hình trong file `.env` trước khi sử dụng mô hình LLM.
- Nếu cần mở rộng chức năng, hãy chỉnh sửa các script trong thư mục `src/data`.

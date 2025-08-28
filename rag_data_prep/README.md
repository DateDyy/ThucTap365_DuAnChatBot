# Chatbot RAG Cho lập trình Web

Dự án này triển khai một chatbot sử dụng kỹ thuật RAG (Retrieval-Augmented Generation) nhằm hỗ trợ người dùng học lập trình web. Chatbot tận dụng thông tin được trích xuất từ tập hợp các tài liệu PDF liên quan đến lập trình web.

## Cấu trúc dự án

```
ThucTap365_DuAnChatBot
├── rag_data_prep
│   ├── src
│   │   ├── main.py                # Điểm khởi chạy chính của ứng dụng chatbot
│   │   ├── rag
│   │   │   ├── retriever.py       # Lớp chịu trách nhiệm tải và truy xuất thông tin từ các PDF
│   │   │   ├── generator.py       # Lớp tạo phản hồi dựa trên thông tin đã truy xuất
│   │   │   └── utils.py           # Các hàm tiện ích xử lý và định dạng văn bản
│   │   ├── data
│   │   │   ├── process_pdf.py     # Các hàm xử lý file PDF và trích xuất văn bản
│   │   │   └── label_data.py      # Các hàm gán nhãn và làm sạch dữ liệu đã trích xuất
│   │   └── config
│   │       └── settings.py        # # Cấu hình cho ứng dụng
│   ├── README.md                  # Tài liệu mô tả dự án
├── pdfs
│   ├── web_programming_1.pdf      # PDF containing web programming content
│   ├── web_programming_2.pdf      # PDF containing web programming content
│   ├── web_programming_3.pdf      # PDF containing web programming content
│   ├── web_programming_4.pdf      # PDF containing web programming content
│   └── web_programming_5.pdf      # PDF containing web programming content
├── processed
│   ├── data_combined.json         # Dữ liệu văn bản đã trích xuất từ các PDF
│   └── data_labeled.json          # Dữ liệu đã được gán nhãn và làm sạch để huấn luyện chatbot
├── requirements.txt               # Danh sách các thư viện cần thiết cho dự án
└── README.md                      # Documentation for the project
```

## Hướng Dẫn Cài Đặt

1. Clone kho lưu trữ::
   ```
   git clone <repository-url>
   cd ThucTap365_DuAnChatBot
   ```

2. Cài đặt các thư viện cần thiết:
   ```
   pip install -r requirements.txt
   ```

3. Đảm bảo rằng các file PDF nằm trong thư mục pdfs.

## Hướng Dẫn Sử Dụng

Để chạy chatbot, thực thi lệnh sau:
```
python rag_data_prep/src/main.py
```

Chatbot sẽ khởi tạo và yêu cầu bạn nhập câu hỏi. Bạn có thể đặt các câu hỏi liên quan đến lập trình web, và chatbot sẽ phản hồi dựa trên thông tin đã được trích xuất từ các tài liệu PDF.

## Tổng quan chức năng

- **Retriever**: Tải các file PDF và tìm kiếm thông tin liên quan dựa trên truy vấn của người dùng.
- **Generator**: Sinh câu trả lời mạch lạc dựa trên thông tin đã truy xuất.
- **Utilities**: Cung cấp các hàm hỗ trợ xử lý và định dạng văn bản.
- **PDF Processing**: Trích xuất văn bản từ các file PDF để chuẩn bị dữ liệu cho retriever.
- **Labeling & Cleaning**: Gán nhãn chủ đề và làm sạch dữ liệu để nâng cao hiệu quả của chatbot.

Dự án này nhằm mục tiêu nâng cao trải nghiệm học tập cho người dùng quan tâm đến lập trình web bằng cách cung cấp một chatbot tương tác và giàu thông tin.
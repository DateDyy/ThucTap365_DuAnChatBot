class Generator:
    def __init__(self):
        pass

    def generate_response(self, retrieved_info):
        """
        Sinh phản hồi dựa trên thông tin đã truy xuất.
        :param retrieved_info: Chuỗi văn bản chứa thông tin liên quan từ retriever
        :return: Chuỗi phản hồi cho người dùng
        """
        if not retrieved_info or retrieved_info.strip() == "":
            return "Xin lỗi, tôi không tìm thấy thông tin phù hợp với câu hỏi của bạn."

        # Có thể bổ sung thêm logic NLP nâng cao ở đây (ví dụ: tóm tắt, RAG)
        response = f"Dựa trên tài liệu, tôi tìm thấy thông tin sau:\n{retrieved_info}"
        return response

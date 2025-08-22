class Retriever:
    def __init__(self, pdf_paths):
        self.pdf_paths = pdf_paths
        self.documents = []

    def load_pdfs(self):
        from src.data.process_pdf import extract_text_from_pdf
        for pdf_path in self.pdf_paths:
            text = extract_text_from_pdf(pdf_path)
            self.documents.append(text)

    def get_relevant_info(self, query):
        # Implement a simple keyword matching or a more complex retrieval method
        relevant_docs = []
        for doc in self.documents:
            if query.lower() in doc.lower():
                relevant_docs.append(doc)
        return relevant_docs
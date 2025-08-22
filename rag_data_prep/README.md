# Chatbot RAG for Web Programming

This project implements a chatbot using Retrieval-Augmented Generation (RAG) techniques to assist users in learning web programming. The chatbot leverages information extracted from a set of PDF documents related to web programming.

## Project Structure

```
chatbot-rag-web-programming
├── src
│   ├── main.py                # Entry point of the chatbot application
│   ├── rag
│   │   ├── retriever.py       # Class for loading and retrieving information from PDFs
│   │   ├── generator.py       # Class for generating responses based on retrieved information
│   │   └── utils.py           # Utility functions for text processing and formatting
│   ├── data
│   │   └── process_pdf.py     # Functions to process PDF files and extract text
│   └── config
│       └── settings.py        # Configuration settings for the application
├── pdfs
│   ├── web_programming_1.pdf  # PDF containing web programming content
│   ├── web_programming_2.pdf  # PDF containing web programming content
│   ├── web_programming_3.pdf  # PDF containing web programming content
│   ├── web_programming_4.pdf  # PDF containing web programming content
│   └── web_programming_5.pdf  # PDF containing web programming content
├── requirements.txt           # List of dependencies required for the project
└── README.md                  # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd chatbot-rag-web-programming
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Ensure that the PDF files are located in the `pdfs` directory.

## Usage Guidelines

To run the chatbot, execute the following command:
```
python src/main.py
```

The chatbot will initialize and prompt you for input. You can ask questions related to web programming, and the chatbot will provide responses based on the information extracted from the PDF documents.

## Overview of Functionality

- **Retriever**: Loads the PDF files and retrieves relevant information based on user queries.
- **Generator**: Generates coherent responses using the retrieved information.
- **Utilities**: Provides helper functions for text processing and formatting.
- **PDF Processing**: Extracts text from PDF files to prepare data for the retriever.

This project aims to enhance the learning experience for users interested in web programming by providing an interactive and informative chatbot.
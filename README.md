# Multilingual-PDF-RAG-System


## Description

The Multilingual PDF Retrieval-Augmented Generation (RAG) System is designed to efficiently process and extract information from PDFs in multiple languages. This innovative solution enables users to obtain summaries and answers from documents in Hindi, English, Bengali, and Chinese, catering to diverse information needs.

## Technology Stack

- **Azure Functions**: For serverless processing of PDF uploads and queries.
- **Cosmos DB**: To store and retrieve extracted content seamlessly.
- **Azure Data Lake**: For scalable storage of PDFs.
- **OpenAI API**: Powers intelligent responses and summarization.
- **Python**: Utilizes libraries like PyMuPDF and Tesseract for text extraction.

## How It Works

1. **PDF Upload**: Users upload documents to Azure Data Lake.
2. **Processing**: Azure Functions extract text using OCR and other methods.
3. **Storage**: Extracted data is chunked and stored in Cosmos DB.
4. **User Interaction**: Users submit queries to retrieve relevant information.
5. **Response Generation**: Responses are crafted using the OpenAI API.

## Features

- Multilingual support for diverse languages.
- Efficient text extraction from both scanned and digital PDFs.
- Future plans for enhanced search capabilities and memory features.

## Future Enhancements

Ongoing improvements include semantic search integration and advanced query handling to elevate user experience.

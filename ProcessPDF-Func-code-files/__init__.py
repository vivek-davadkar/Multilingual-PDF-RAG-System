import logging
import azure.functions as func
from azure.cosmos import CosmosClient
import uuid
import pytesseract
from pdf2image import convert_from_bytes
from langdetect import detect
import fitz  # PyMuPDF

# Initialize Cosmos DB clients
cosmos_endpoint = "YOUR_COSMOS_ENDPOINT"  # e.g., "https://your-cosmos-account.documents.azure.com:443/"
cosmos_key = "YOUR_COSMOS_KEY"  # Your actual Cosmos DB key
database_name = "rag_documents"
container_name = "documents"

cosmos_client = CosmosClient(cosmos_endpoint, cosmos_key)

def main(blob: func.InputStream):
    logging.info(f"Processing blob: {blob.name}, Size: {blob.length} bytes")

    try:
        # Read the blob content
        pdf_content = blob.read()
        logging.info("File downloaded successfully. Extracting text...")

        extracted_text = extract_text_from_pdf(pdf_content)

        # Detect language from the extracted text
        detected_language = detect(extracted_text)
        lang_code = get_language_code(detected_language)

        logging.info(f"Detected language: {detected_language} (Tesseract code: {lang_code})")

        # If the text is scanned, re-extract text with detected language
        if not any(char.isascii() for char in extracted_text):  # Check if the text is non-ASCII
            images = convert_from_bytes(pdf_content)
            extracted_text = ""
            for image in images:
                extracted_text += pytesseract.image_to_string(image, lang=lang_code)

        logging.info("Text extraction complete. Chunking text...")
        chunks = [extracted_text[i:i + 500] for i in range(0, len(extracted_text), 500)]

        # Upload chunks to Cosmos DB
        database = cosmos_client.get_database_client(database_name)
        container = database.get_container_client(container_name)

        for chunk in chunks:
            container.upsert_item({'id': str(uuid.uuid4()), 'content': chunk})

        logging.info("Chunks uploaded to Cosmos DB successfully.")

    except Exception as e:
        logging.error("Error processing PDF", exc_info=True)

def extract_text_from_pdf(pdf_content):
    """Extract text from a PDF file using PyMuPDF."""
    try:
        pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
        text = ""
        for page in pdf_document:
            text += page.get_text()
        return text
    except Exception as e:
        logging.error("Error extracting text from PDF", exc_info=True)
        return ""

def get_language_code(detected_language):
    """Map detected language to Tesseract language codes."""
    language_map = {
        'en': 'eng',  # English
        'hi': 'hin',  # Hindi
        'bn': 'ben',  # Bengali
        'zh': 'chi',  # Chinese
        'ur': 'urd'   # Urdu
    }
    return language_map.get(detected_language, 'eng')  # Default to English if not found

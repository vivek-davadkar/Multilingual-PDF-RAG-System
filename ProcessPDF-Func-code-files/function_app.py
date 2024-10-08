import azure.functions as func
import logging

# The function doesn't need to be defined under a FunctionApp since it's a blob trigger
def main(blob: func.InputStream) -> None:
    logging.info(f"Blob trigger function processed blob: {blob.name}, Size: {blob.length} bytes")
    
    try:
        # Here you can add your logic to process the blob
        blob_content = blob.read()
        # Add your PDF processing logic here
        logging.info(f"Processing blob content: {blob_content}")
        
    except Exception as e:
        logging.error(f"Error processing blob {blob.name}: {e}", exc_info=True)

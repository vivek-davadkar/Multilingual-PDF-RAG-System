import azure.functions as func
import logging

app = func.FunctionApp()

@app.route(route="QueryAndGenerateResponse", auth_level=func.AuthLevel.ANONYMOUS)
def QueryAndGenerateResponse(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Query and generate response function triggered.')

    try:
        user_query = req.params.get('query')
        if not user_query:
            req_body = req.get_json()
            user_query = req_body.get('query')

        if not user_query:
            return func.HttpResponse("Please pass a query", status_code=400)

        # Call your existing logic here to query the documents
        return main(req)  # Ensure this matches your original logic

    except Exception as e:
        logging.error(f"Error querying documents: {e}", exc_info=True)
        return func.HttpResponse("Error querying documents", status_code=500)

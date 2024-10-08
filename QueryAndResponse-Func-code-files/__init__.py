import logging
import azure.functions as func
from azure.cosmos import CosmosClient
import openai

# Initialize OpenAI and Cosmos DB clients
cosmos_endpoint = "https://YOUR_COSMOS_ACCOUNT.documents.azure.com:443/"
cosmos_key = "YOUR_COSMOS_KEY"
database_name = "rag_documents"
container_name = "documents"
openai.api_key = "YOUR_OPENAI_API_KEY"
openai.api_base = "https://YOUR_OPENAI_ENDPOINT/"

cosmos_client = CosmosClient(cosmos_endpoint, cosmos_key)

def query_documents(query):
    database = cosmos_client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    sql_query = f"SELECT * FROM c WHERE CONTAINS(c.content, '{query}')"
    return list(container.query_items(query=sql_query, enable_cross_partition_query=True))

def generate_answer(search_results, user_query):
    combined_context = " ".join([res['content'] for res in search_results])
    prompt = f"Based on the following context: {combined_context}\nAnswer the following question: {user_query}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        n=1
    )
    return response['choices'][0]['text']

def main(req: func.HttpRequest) -> func.HttpResponse:
    user_query = req.params.get('query')
    if not user_query:
        return func.HttpResponse("Please pass a query", status_code=400)

    search_results = query_documents(user_query)
    response = generate_answer(search_results, user_query)
    return func.HttpResponse(response)

import os
import json
import openai
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential


# Creeer een functie die de embeddings van de content te verkrijgt
def get_embeddings(contents):
    embeddings = []
    for content in contents:
        response = openai.Embedding.create(input=[content], model='text-embedding-ada-002')
        embeddings.append(response['data'][0]['embedding'])
    return embeddings


def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Laad de schoongemaakte data
    with open('../data-cleaning/cleaned_data.json', 'r') as f:
        cleaned_data = json.load(f)

    # Haal de content uit de data en roep de functie aan om de embeddings te verkrijgen
    contents = [item['content'] for item in cleaned_data]  # Assuming your JSON has a 'content' key
    embeddings = get_embeddings(contents)

    # Initialiseer de SearchClient
    service_endpoint = os.getenv("AI_SEARCH_ENDPOINT")
    index_name = "erasmusbot-index"
    credential = AzureKeyCredential(os.getenv("AZURE_AI_SEARCH_KEY"))
    search_client = SearchClient(endpoint=service_endpoint, index_name=index_name, credential=credential)

    # Bereid de pagina's voor om te uploaden
    pages = [{"id": str(i), "title": item['title'], "source": item['source'], "description": item['description'], "content": item['content'], "embedding": embeddings[i]} for i, item in enumerate(cleaned_data)]

    # Upload de pagina's
    search_client.upload_documents(pages)


if __name__ == "__main__":
    main()
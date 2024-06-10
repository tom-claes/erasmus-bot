import os
import json
import openai
from azure.search.documents.indexes.models import SimpleField, SearchIndex, SearchFieldDataType
from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient


# Initialize the index client
service_endpoint = os.getenv("AI_SEARCH_ENDPOINT")
credential = AzureKeyCredential(os.getenv("AZURE_KEY"))
index_client = SearchIndexClient(endpoint=service_endpoint, credential=credential)
openai.api_key = 'your_openai_api_key'

# Define the index schema
index_name = "erasmusbot-index"
index_schema = SearchIndex(
    name=index_name,
    fields=[
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SimpleField(name="content", type=SearchFieldDataType.String, searchable=True),
        SimpleField(name="embedding", type=SearchFieldDataType.Collection(SearchFieldDataType.Double))
    ]
)

# Create the index
index_client.create_index(index_schema)

# create the index - stop






# Load cleaned data
with open('../data-cleaning/cleaned_data.json', 'r') as f:
    cleaned_data = json.load(f)

# Function to get embeddings
def get_embeddings(texts):
    embeddings = []
    for text in texts:
        response = openai.Embedding.create(input=[text], model='text-embedding-ada-002')
        embeddings.append(response['data'][0]['embedding'])
    return embeddings

texts = [item['content'] for item in cleaned_data]  # Assuming your JSON has a 'content' key
embeddings = get_embeddings(texts)




# Initialize the search client
search_client = SearchClient(endpoint=service_endpoint, index_name=index_name, credential=credential)

# Prepare documents for upload
documents = [{"id": str(i), "content": texts[i], "embedding": embeddings[i]} for i in range(len(texts))]

# Upload documents
search_client.upload_documents(documents)



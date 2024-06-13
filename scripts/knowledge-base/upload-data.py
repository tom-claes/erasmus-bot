import os
import json
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# Define the directory containing the text files
directory = 'final-data'

# Initialize the list of documents
documents = []

# Iterate over each file in the directory
for filename in os.listdir(directory):
    # Only process .txt files
    if filename.endswith('.txt'):
        # Construct the full file path
        file_path = os.path.join(directory, filename)

        try:
            # Open the file and load the JSON content
            with open(file_path, 'r') as f:
                document = json.load(f)

            # Add the document to the list
            documents.append(document)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")


# Define the search endpoint and index name
search_endpoint = os.getenv("AI_SEARCH_ENDPOINT")
index_name = "erasmusbot-index"

# Define the credential
credential = AzureKeyCredential(os.getenv("AZURE_AI_SEARCH_KEY"))

# Initialize the search client
search_client = SearchClient(endpoint=search_endpoint,
                             index_name=index_name,
                             credential=credential)

# Upload the documents to the index
for document in documents:
    try:
        result = search_client.upload_documents(documents=[document])
        print("Upload of new document succeeded: {}".format(result[0].succeeded))
    except Exception as ex:
        print(f"Error uploading document {document['id']}: {ex}")
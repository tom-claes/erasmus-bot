# Importeer de benodigde libraries
import os
from azure.search.documents.indexes.models import SimpleField, SearchIndex, SearchFieldDataType
from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential


def main():
    # Initialiseer de index client
    service_endpoint = os.getenv("AI_SEARCH_ENDPOINT")
    credential = AzureKeyCredential(os.getenv("AZURE_AI_SEARCH_KEY"))
    index_client = SearchIndexClient(endpoint=service_endpoint, credential=credential)

    # Definieer het index schema
    index_name = "erasmusbot-index"
    index_schema = SearchIndex(
        name=index_name,
        fields=[
            SimpleField(name="id", type=SearchFieldDataType.String, key=True),
            SimpleField(name="title", type=SearchFieldDataType.String, searchable=True),
            SimpleField(name="source", type=SearchFieldDataType.String),
            SimpleField(name="description", type=SearchFieldDataType.String, searchable=True),
            SimpleField(name="content", type=SearchFieldDataType.String, searchable=True),
            SimpleField(name="embedding", type=SearchFieldDataType.Collection(SearchFieldDataType.Double))
        ]
    )

    # Creëer de index
    index_client.create_index(index_schema)


if __name__ == "__main__":
    main()




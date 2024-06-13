import os
import json
import re
from openai import AzureOpenAI


def get_embeddings(cleaned_data):
    embeddings = []

    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version="2024-02-01",
        azure_endpoint=os.getenv("OPENAI_ENDPOINT")
    )

    for data in cleaned_data:
        content = data['content']
        response = client.embeddings.create(
            input=content,
            model="erasmusbot-embeddings"
        )
        embeddings.append(response.model_dump_json(indent=2))
    return embeddings


def save_data(cleaned_data, embeddings):
    output_directory='final-data'

    # Create the directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Dictionary to keep track of title counts
    title_counts = {}

    # Iterate over cleaned_data and embeddings
    for i, item in enumerate(cleaned_data):
        try:
            # Assuming `item` is your data
            embedding_str = item['embedding']

            # Parse the string into a JSON object
            embedding_json = json.loads(embedding_str)

            # Extract the embedding array
            embedding_values = embedding_json['data'][0]['embedding']

            # Assign it back to the 'embedding' field
            item['embedding'] = embedding_values

            # Create the object
            page = {
                    "id": str(i),
                    "title": item['title'],
                    "source": item['source'],
                    "description": item['description'],
                    "content": item['content'],
                    "embedding": item['embedding'],
                }

            # Convert the title to a filename format
            filename = re.sub('[^a-zA-Z0-9()]', '-', item['title'])

            # Check if the title already exists
            if filename in title_counts:
                title_counts[filename] += 1
                filename = f"{filename}-{title_counts[filename]}"
            else:
                title_counts[filename] = 1

            # Define the file path
            file_path = os.path.join(output_directory, f'{filename}.txt')

            # Write the object to the file
            with open(file_path, 'w') as f:
                json.dump(page, f, indent=4)

            print(f"Saved file {file_path}")

        except Exception as e:
            print(f"An error occurred while processing item {i}: {e}")

    print(f"Processed {len(cleaned_data)} items")


def main():
    # Laad de schoongemaakte data
    with open('../data-cleaning/cleaned_data.json', 'r', encoding='utf-8') as f:
        cleaned_data = json.load(f)

    embeddings = get_embeddings(cleaned_data)

    save_data(cleaned_data, embeddings)


if __name__ == "__main__":
    main()
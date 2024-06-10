import json

# Open the file
with open('cleaned_data.json', 'r') as json_file:
    # Load the data
    cleaned_data = json.load(json_file)

# Now you can access the data
print(cleaned_data)
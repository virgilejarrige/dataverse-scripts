import requests

# Set the base URL of your Dataverse installation
base_url = "https://entrepot.recherche.data.gouv.fr/api"

# Set the API token for authentication
api_token = "your-secret-token"

# Set the collection to search within
collection = "root"  # Replace with the desired collection identifier

# Define the string to match in the affiliation
target_affiliation = "CNRS"

# Set the search API endpoint
search_endpoint = f"{base_url}/search"

# Define headers for API requests
headers = {
    "X-Dataverse-key": api_token,
    "Content-type": "application/json"
}

# Define the search parameters
params = {
    "q": "*",
    "type": "dataset",
    "subtree": collection,
    "metadata_fields": "citation:*"
}

# Send a GET request to search for datasets within the specified collection
response = requests.get(search_endpoint, params=params, headers=headers)

# Check if the request was successful (HTTP status code 200)
if response.status_code == 200:
    # Retrieve the JSON data from the response
    data = response.json()

    # Extract the dataset items from the response
    datasets = data["data"]["items"]

    # Iterate over each dataset and print its title and affiliation
    for dataset in datasets:
        title = dataset["name"]
        metadata_blocks = dataset["metadataBlocks"]
        
        # Extract the affiliation from the metadata blocks
        affiliation = None
        if "citation" in metadata_blocks and "fields" in metadata_blocks["citation"]:
            fields = metadata_blocks["citation"]["fields"]
            for field in fields:
                if "datasetContactAffiliation" in field["value"][0]:
                    affiliation = field["value"][0]["datasetContactAffiliation"]["value"]
                    break
        
        # Check if the affiliation contains the specified string
        if affiliation and target_affiliation in affiliation:
            print("Title:", title)
            print("Affiliation:", affiliation)
            print("---")
else:
    print("Error:", response.text)

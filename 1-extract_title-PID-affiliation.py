import csv
import requests

# Modify these variables
# Set the base URL of your Dataverse installation
base_url = "https://datavers_url.com/api"

# Set the API token for authentication
api_token = "your_secret_token"

# Set the collection to search within
collection = "collection_id"  # Replace with the desired collection identifier

#-------------------------------------
# Don't modify any further!
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

    # Create a CSV file to store the results
    csv_filename = f"dataset_title_affiliation_{collection}.csv"
    with open(csv_filename, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Affiliation", "Global ID"])

        # Iterate over each dataset and write its title, affiliation, and global ID to the CSV file
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

            global_id = dataset["global_id"]

            writer.writerow([title, affiliation, global_id])

    print(f"CSV file '{csv_filename}' has been created.")
else:
    print("Error:", response.text)

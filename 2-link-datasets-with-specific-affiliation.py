import csv
import requests

# Modify these variables
# Set the base URL of your Dataverse installation
base_url = "https://dataverse_url.com/api"

# Set the API token for authentication
api_token = "your_secret_token"

# Set the CSV file path
csv_filename = "dataset_title_affiliation_collectionid.csv"  # Update with the appropriate CSV filename

# Set the target collection ID
collection_id = "target_collection"  # Replace with the ID of the desired collection

# Set the affiliation pattern to be matched
affiliation_pattern = "pattern"  # Update with the desired affiliation pattern

#---------------------------
# Don't modify any further
# Define headers for API requests
headers = {
    "X-Dataverse-key": api_token,
    "Content-type": "application/json"
}

# Read the CSV file and link datasets with the defined affiliation pattern to the collection
with open(csv_filename, mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    header = next(reader)  # Skip the header row
    datasets = list(reader)

    # Iterate over each dataset and link it to the collection based on the defined affiliation pattern
    for dataset in datasets:
        title, affiliation, global_id = dataset

        # Check if the affiliation pattern is found in the dataset's affiliation
        if affiliation_pattern in affiliation:
            # Get the dataset ID from the persistent identifier
            dataset_endpoint = f"{base_url}/datasets/:persistentId/"
            params = {
                "persistentId": global_id
            }
            response = requests.get(dataset_endpoint, params=params, headers=headers)
            data = response.json()
            dataset_id = data["data"]["id"]

            # Create the link API endpoint
            link_endpoint = f"{base_url}/datasets/{dataset_id}/link/{collection_id}"

            # Send a PUT request to link the dataset to the collection
            response = requests.put(link_endpoint, headers=headers)

            # Check if the request was successful (HTTP status code 200)
            if response.status_code == 200:
                print(f"Dataset '{title}' linked to collection with ID '{collection_id}'")
            else:
                print(f"Failed to link dataset '{title}' to collection with ID '{collection_id}': {response.text}")
        else:
            print(f"Skipping dataset '{title}' as it does not match the affiliation pattern")

print("Linking process completed.")

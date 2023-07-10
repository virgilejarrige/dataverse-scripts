import csv
import requests

# Modify these variables
# Set the base URL of your Dataverse installation
base_url = "https://datavers_url.com"

# Set the API token for authentication
api_token = "your_secret_token"

# Set the collection to search within
collection = "collection_id"  # Replace with the desired collection identifier

#-------------------------------------
# Don't modify any further!
# Set the search API endpoint
search_endpoint = f"{base_url}/api/search"

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
    "metadata_fields": "citation:*",
    "per_page": "100",
    "start": "0"
}

# Send the initial request to retrieve the first page of results
response = requests.get(search_endpoint, params=params, headers=headers)

# Check if the request was successful (HTTP status code 200)
if response.status_code == 200:
    # Retrieve the JSON data from the response
    data = response.json()

    # Get the total count of results
    total_count = data['data']['total_count']
    print("Total results:", total_count)

    # Create a CSV file to store the results
    csv_filename = f"dataset_title_affiliation_{collection}.csv"
    with open(csv_filename, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Affiliation", "Global ID"])

        # Iterate until all results are retrieved
        start = 0
        retrieved_count = 0
        while start < total_count:
            params["start"] = str(start)
            response = requests.get(search_endpoint, params=params, headers=headers)

            # Check if the request was successful (HTTP status code 200)
            if response.status_code == 200:
                # Retrieve the JSON data from the response
                data = response.json()

                # Extract the dataset items from the response
                datasets = data["data"]["items"]

                # Iterate over each dataset and write its title, affiliation, and global ID to the CSV file
                for dataset in datasets:
                    title = dataset["name"]
                    metadata_blocks = dataset["metadataBlocks"]

                    # Extract the affiliation from the metadata blocks
                    affiliation = None
                    if "citation" in metadata_blocks and "fields" in metadata_blocks["citation"]:
                        fields = metadata_blocks["citation"]["fields"]
                        for field in fields:
                            if "datasetContactAffiliation" in field.get("value", []):
                                affiliation = field["value"][0]["datasetContactAffiliation"]["value"]
                                break

                    global_id = dataset["global_id"]

                    # Escape the commas in the title
                    title = title.replace(",", "\\,")

                    writer.writerow([title, affiliation, global_id])

                    retrieved_count += 1

                start += len(datasets)

                # Calculate the remaining datasets
                remaining_count = total_count - retrieved_count
                print(f"Retrieved: {retrieved_count} | Remaining: {remaining_count}")
            else:
                print(f"Error retrieving datasets: {response.text}")
                break

    print(f"CSV file '{csv_filename}' has been created.")
else:
    print("Error:", response.text)

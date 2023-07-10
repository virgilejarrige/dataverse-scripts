import csv
import requests
import json

# Read user variables from the text file
with open("user_variables.txt", mode="r") as var_file:
    user_variables = var_file.read()

# Evaluate the user variables as Python code
exec(user_variables)

#---------------------------
# Don't modify any further
# Define headers for API requests
headers = {
    "X-Dataverse-key": api_token,
    "Content-type": "application/json"
}

# Read the CSV file and link datasets with the defined affiliation pattern to the target collection
with open(csv_filename, mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    header = next(reader)  # Skip the header row
    datasets = list(reader)

    # Iterate over each dataset and link it to the target collection based on the defined affiliation pattern
    for dataset in datasets:
        title, affiliation, global_id = dataset

        # Check if the affiliation pattern is found in the dataset's affiliation
        if affiliation_pattern in affiliation:
            # Get the dataset ID from the persistent identifier
            dataset_endpoint = f"{base_url}/api/datasets/:persistentId/"
            params = {
                "persistentId": global_id
            }
            try:
                response = requests.get(dataset_endpoint, params=params, headers=headers)
                data = response.json()
                dataset_id = data["data"]["id"]

                # Create the link API endpoint
                link_endpoint = f"{base_url}/api/datasets/{dataset_id}/link/{target_collection}"

                # Send a PUT request to link the dataset to the target collection
                response = requests.put(link_endpoint, headers=headers)

                # Check if the request was successful (HTTP status code 200)
                if response.status_code == 200:
                    print(f"Dataset '{title}' linked to collection with ID '{target_collection}'")
                else:
                    print(f"Failed to link dataset '{title}' to collection with ID '{target_collection}': {response.text}")
            except json.JSONDecodeError as e:
                print(f"Failed to parse the JSON response for dataset '{title}': {e}")
        else:
            print(f"Skipping dataset '{title}' as it does not match the affiliation pattern")

print("Linking process completed.")

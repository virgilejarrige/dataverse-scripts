import csv
import requests
import json
import os

# Read user variables from the text file
with open("user_variables.py", mode="r") as var_file:
    user_variables = var_file.read()

# Evaluate the user variables as Python code
exec(user_variables)

# Define headers for API requests
headers = {
    "X-Dataverse-key": api_token,
    "Content-type": "application/json"
}

# Get a list of all CSV files in the current directory
csv_files = [file for file in os.listdir(".") if file.endswith(".csv")]

# Ask the user to choose which CSV file to use
print("Choose a CSV file to use:")
for i, csv_file in enumerate(csv_files):
    print(f"{i + 1}. {csv_file}")

choice = int(input("Enter the number corresponding to the CSV file: ")) - 1
csv_filename = csv_files[choice]

# Read the CSV file and link datasets with the defined affiliation pattern to the target collection
with open(csv_filename, mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    header = next(reader)  # Skip the header row
    datasets = list(reader)

# Make the pattern case-insensitive
affiliation_pattern = affiliation_pattern.lower()

# Iterate over each dataset and link it to the target collection based on the defined affiliation pattern
for dataset in datasets:
    title, affiliation, producer, global_id = dataset

    # Check if the affiliation pattern is found in the dataset's affiliation or producer (case-insensitive)
    if affiliation_pattern in affiliation.lower() or affiliation_pattern in producer.lower():
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

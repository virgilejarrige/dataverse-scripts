import csv
import requests

# Read user variables from the text file
with open("user_variables.py", mode="r") as var_file:
    user_variables = var_file.read()

# Evaluate the user variables as Python code
exec(user_variables)

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
    "start": 0,
    "per_page": 100
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
        page = 1
        while start < total_count:
            print(f"Retrieving page {page} - {start+1} to {min(start+params['per_page'], total_count)}")
            params["start"] = start
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

                    # Initialize affiliation to None
                    affiliation = None

                    try:
                        # Extract the affiliation from the metadata blocks
                        if "citation" in metadata_blocks and "fields" in metadata_blocks["citation"]:
                            fields = metadata_blocks["citation"]["fields"]
                            for field in fields:
                                if "datasetContactAffiliation" in field["value"][0]:
                                    affiliation = field["value"][0]["datasetContactAffiliation"]["value"]
                                    break
                    except KeyError:
                        pass

                    global_id = dataset["global_id"]

                    # Escape the commas in the title and affiliation, enclosing them in double quotation marks
                    title = title.replace(",", "\\,").replace('"', '""')
                    if affiliation:
                        affiliation = affiliation.replace(",", "\\,").replace('"', '""')

                    writer.writerow([f'"{title}"', f'"{affiliation}"', global_id])

                start += len(datasets)
                page += 1
            else:
                print(f"Error retrieving page {page}: {response.text}")
                break

    print(f"CSV file '{csv_filename}' has been created.")
else:
    print("Error:", response.text)

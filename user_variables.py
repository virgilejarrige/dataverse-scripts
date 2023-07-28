# Configuration variables for the script

# Set the base URL of your Dataverse installation
base_url = "https://demo.dataverse.org"

# Set the API token for authentication
api_token = "your_secret_token"

#---

#Script #1 only
# Set collection ID
collection = "root"  # Replace with the ID of the collection

#---

#Script #2 only
# Set the source collection ID
collection_id = "root"  # Replace with the ID of the source collection

# Set the CSV file path
csv_filename = "dataset_title_affiliation_collectionid.csv"  # Update with the appropriate CSV filename

# Set the target collection ID
target_collection = "target_collection"  # Replace with the ID of the desired target collection

# Set the affiliation pattern to be matched
affiliation_pattern = "pattern"  # Update with the desired affiliation pattern


#----

#random-file-uploader and download_files.py

# Set the DOI of the dataset in which you want to send random files to or in which you want to download files.
DOI = "doi:10.xxxxx/xxxxx"

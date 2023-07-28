#1. Import the necessary modules
from pyDataverse.api import NativeApi, DataAccessApi

# Read user variables from the text file                     
with open("user_variables.py", mode="r") as var_file:                   
    user_variables = var_file.read()                 

# Evaluate the user variables as Python code                            
exec(user_variables)                                     

# Create a NativeApi instance                                           
api = NativeApi(base_url, api_token)   

#5. Retrieve the existing Dataset using its DOI
dataset = api.get_dataset(DOI)

#6. Create a DataAccessApi instance
data_api = DataAccessApi(base_url)

#7. Get the list of files in the Dataset
files_list = dataset.json()['data']['latestVersion']['files']

#8. Display the list of files with index numbers
print("List of available files:")
for i, file_info in enumerate(files_list):
    filename = file_info["dataFile"]["filename"]
    print(f"{i+1}. {filename}")

#9. Ask the user to enter the index numbers of the files to download
selected_files = input("Enter the index numbers of the files to download (separated by spaces): ")
selected_files = selected_files.split()

#10. Download the selected files
for index in selected_files:
    try:
        index = int(index)
        if 1 <= index <= len(files_list):
            file_info = files_list[index - 1]
            file_id = file_info["dataFile"]["id"]
            filename = file_info["dataFile"]["filename"]

            print("Downloading file:", filename)

            # 11. Use the get_datafile() method to download the file
            response = data_api.get_datafile(file_id)

            # 12. Save the file locally
            with open(filename, "wb") as f:
                f.write(response.content)

            print("File", filename, "has been successfully downloaded.")
        else:
            print("Invalid index number. Ignored.")
    except ValueError:
        print("Please enter valid index numbers. Ignored.")

print("Download of selected files completed.")

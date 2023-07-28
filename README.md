# dataverse-scripts
Generic scripts to be used with dataverse - https://github.com/IQSS/dataverse

## Clone the repository and modify user_variables.py with your informations. 

## 1-extract_title-PID-affiliation.py
Will extract the title, affiliation and PID of all the datasets of a specific collection to a csv file
## 2-link-datasets-with-specific-affiliation.py
Will link all the datasets with a specific affiliation to a specific collection, based on the csv that 1-extract_title-PID-affiliation.py generates
## random_files_upload.py
Randomly generates 5 files (csv, jpg or txt) of 500kb to 1Mb and then uploads them to a specific dataset
pip install faker reportlab pandas pillow pyDataverse
## download_files.py
Allows to download files based on user input. All files of a dataset are displayed, and the user chosses which ones he wants to download.

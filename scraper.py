import os
import shutil
import requests
import json


def get_schedule():
    # Load credentials from JSON file
    with open("/home/ubuntu/deployed_project/scraper_owncloud_geomatique/json/credentials.json", "r") as json_file:
        credentials = json.load(json_file)
        username = credentials["username"]
        password = credentials["password"]
        file_url = credentials["file_url"]
        download_directory = credentials["download_directory"]

    # Specify the download directory and file path

    file_name = "spreadsheet.xlsx"

    # Create a session to handle authentication
    session = requests.Session()
    session.auth = (username, password)

    # Download the file
    response = session.get(file_url, stream=True)
    if response.status_code == 200:
        with open(os.path.join(download_directory, file_name), 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
            print("file downloaded to : ", download_directory)
    else:
        print("Failed to download the file.")

    # Close the session
    session.close()

# Script to generate `.txt` files for finetuning
# Pulls all files from the postgres source repo (https://github.com/postgres/postgres) and also the postgres docs (www.postgresql.org/)
# Could also pull from internal data that we have at Tembo.io

import os
import re
import requests
from bs4 import BeautifulSoup

# Define the GitHub repository URL
repo_url = "https://github.com/postgres/postgres"

# Send a GET request to the repository URL
response = requests.get(repo_url)

# Check if the request was successful
if response.status_code == 200:
    # Find all file links on the page
    file_links = []

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    file_links = [a['href'] for a in soup.find_all('a', class_='js-navigation-open')]

    file_links = [link for link in file_links if '.' in link]

    file_links = [f"{link.replace('/blob', '')}" for link in file_links]



    for link in file_links:

        # Get the raw content URL
        raw_url = f"https://raw.githubusercontent.com{link}"

        # Fetch the file content
        file_response = requests.get(raw_url)

        if file_response.status_code == 200:
            # Extract the file name from the file path
            file_name = os.path.basename(link)

            # Change the file extension to .txt
            txt_file_name = os.path.splitext(file_name)[0] + ".txt"

            # Create the actual file

            # Save the content to a .txt file in the data directory
            with open(os.path.join("finetune/data", txt_file_name), "w") as txt_file:
                txt_file.write(file_response.text)

            print(f"Saved {txt_file_name}")

    print("All files converted and saved in the 'data' directory.")
else:
    print("Failed to fetch the repository page. Please check the URL or your internet connection.")

# Script to generate `.txt` files for finetuning
# Pulls all files from the postgres source repo (https://github.com/postgres/postgres) and also the postgres docs (www.postgresql.org/)
# Could also pull from internal data that we have at Tembo.io
import os
import re
import requests
from bs4 import BeautifulSoup

# Define the GitHub repository URL
base_repo_url = "https://github.com/postgres/postgres"
base_repo_content_url = "https://api.github.com/repos/postgres/postgres/contents/"

token = "<your-token-here>"
username = 'DarrenBaldwin07'

# Create a session with authentication
session = requests.Session()
session.auth = (username, token)

def recurs_scrape(url: str, store):
    response = requests.get(url)
    if response.status_code == 200:
        print('CALLED')
        soup = BeautifulSoup(response.text, 'html.parser')
        non_file_links = [link for link in soup.find_all('a', class_='js-navigation-open') if '.' not in link['href']]
        print(non_file_links)
        for link in soup.find_all('a', class_='js-navigation-open'):
            if '.' in link['href']:
                store.append(link['href'].replace('/blob', ''))
        for link in non_file_links:
            if 'src' in link['href']:
                print(f"{base_repo_url.replace('/postgres/postgres', '')}{link['href']}")
                recurs_scrape(f"{base_repo_url.replace('/postgres/postgres', '')}{link['href']}", store)

def get_all_files_recursive(url, store):
    response = session.get(url)
    if response.status_code == 200:
        data = response.json()
        for item in data:
            if item["type"] == "file":
                store.append(item["html_url"].replace('https://github.com', '').replace('/blob', ''))
            elif item["type"] == "dir":
                get_all_files_recursive(item["url"], store)
    else:
        print(f"Error: {response.status_code}")


def scrape_repo():
    try:
        # Find all file links on the page
        file_links = []

        # Start the process with the repository root
        get_all_files_recursive(base_repo_content_url, file_links)

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

                # Save the content to a .txt file in the data directory
                with open(os.path.join("finetune/data", txt_file_name), "w") as txt_file:
                    txt_file.write(file_response.text)

                print(f"Saved {txt_file_name}")
    except Exception as e:
        print(e)


scrape_repo()

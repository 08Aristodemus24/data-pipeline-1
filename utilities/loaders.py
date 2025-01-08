import requests
import zipfile
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def download_data(page_names_urls):
    # make data folder if one does not already exist
    os.makedirs("./data/", exist_ok=True)

    # define helper for eexcutor
    def helper(row):
        # extract file name adn download url
        file_name, download_url = row

        # make reqquest to endpoint
        response = requests.get(download_url, stream=True)

        # extract primary zip file
        if not os.path.exists(f"./data/{file_name}"):
            with open(f"./data/{file_name}", mode="wb") as file:
                for chunk in tqdm(response.iter_content(chunk_size=10 * 1024)):
                    file.write(chunk)

    # define thread executor to execute downloads concurrently
    with ThreadPoolExecutor() as exe:
        exe.map(helper, page_names_urls)
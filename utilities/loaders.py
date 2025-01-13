import requests
import zipfile
import os
import urllib3
import time

from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


def download_data(page_names_urls):
    # make data folder if one does not already exist
    os.makedirs("./data/", exist_ok=True)

    # define helper for eexcutor
    def helper(row):
        # extract file name adn download url
        file_name, download_url = row
        print(file_name)

        # make reqquest to endpoint
        response = requests.get(download_url, stream=True)
        file_size = int(response['Content-Length'])
        
        downloaded = 0
        # extract primary zip file
        if not os.path.exists(f"./data/{file_name}"):
            with open(f"./data/{file_name}", mode="wb") as file:
                for chunk in tqdm(response.iter_content(chunk_size=1024 * 10)):
                    downloaded += file.write(chunk)
                    now = time.time()

                    # if now - last_print >= 1:
                    #     pct_done = round(downloaded / file_size * 100)
                    #     print(f"download {pct_done}% done\n")
                    #     last_print = time.time()

        # http = urllib3.PoolManager()
        # headers = http.request('HEAD', download_url).headers
        # response = http.request('GET', download_url, preload_content=False)
        # file_size = int(headers['Content-Length'])

        # # downloaded = 0
        # # start = last_print = time.time()
        # # extract primary zip file
        # if not os.path.exists(f"./data/{file_name}"):
        #     with open(f"./data/{file_name}", mode="wb") as file:
        #         for chunk in tqdm(response.stream(1024 * 10)):
        #             downloaded += file.write(chunk)
        #             # now = time.time()

        #             # if now - last_print >= 1:
        #             #     pct_done = round(downloaded / file_size * 100)
        #             #     print(f"download {pct_done}% done\n")
        #             #     last_print = time.time()




    # define thread executor to execute downloads concurrently
    with ThreadPoolExecutor() as exe:
        exe.map(helper, page_names_urls)


# {'Accept-Ranges': 'bytes',
#  'Content-Length': '207323724',
#  'Content-Type': 'application/octet-stream',
#  'Date': 'Thu, 09 Jan 2025 00:36:31 GMT',
#  'ETag': '"8f944ccae28cdbb1249f9153c2e3bb2e"',
#  'Last-Modified': 'Mon, 17 Apr 2023 08:31:56 GMT',
#  'Server': 'WasabiS3/7.21.4957-2024-11-21-b4e1fb3b50',
#  'x-amz-id-2': 'FRGIi1RHPMkjbHqyZQ1KrsiF0jDHX7vazX0U2oZ6TVxAAz7EjenvhsKxFypKP3DM9sJo/DxW3jBQ',
#  'x-amz-meta-mtime': '1526099694',
#  'x-amz-request-id': '4BF959A7D01DCDED:B',
#  'x-wasabi-cm-reference-id': '1736382990121 103.151.85.102 ConID:796839271/EngineConID:7743570/Core:46'}
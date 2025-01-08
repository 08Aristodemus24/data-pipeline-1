import os
import requests
from scipy.io import loadmat
from bs4 import BeautifulSoup
from pathlib import Path
from argparse import ArgumentParser
import re

from utilities.loaders import download_data

# url to download files in each paginator number
# http://gigadb.org/dataset/view/id/100295/Files_page/1
# http://gigadb.org/dataset/view/id/100295/Files_page/2
# ...
# http://gigadb.org/dataset/view/id/100295/Files_page/6

# idea is to loop through each pagination 
# open the link using beautifulsoup or selenium

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--n_pages", type=int, default=1, help="number of pages in the paginator that will be used as basis how many times the crawler should look")
    args = parser.parse_args()

    for page in range(args.n_pages):
        url = 'http://gigadb.org/dataset/view/id/100295/Files_page/{page}'.format(page=page)
        response = requests.get(url)

        # parse response into html
        page = BeautifulSoup(response.text, 'lxml')
        table_body = page.select('div#files tbody')[0]

        # extract the file names
        file_names = [table_row.text for table_row in table_body.select('div[title]')]

        # extract each download link from table
        download_links = [table_row.get('href') for table_row in table_body.select('a.icon-download')]
        page_names_urls = list(zip(file_names, download_links))
        
        # download data
        print(f"downloading batch {page}...")
        download_data(page_names_urls)

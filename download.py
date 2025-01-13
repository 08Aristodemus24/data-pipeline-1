import os
import requests
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
    parser.add_argument("--page_range", type=int, nargs='+', default=[1], help="number of pages in the paginator that will be used as basis how many times the crawler should look")
    args = parser.parse_args()
    start, end = (args.page_range[0], 1) if len(args.page_range) == 1 else (args.page_range[0], args.page_range[-1])

    # start batch download
    for page in range(start, end + 1):
        url = 'http://gigadb.org/dataset/view/id/100295/Files_page/{page}'.format(page=page)
        response = requests.get(url)

        # parse response into html
        doc = BeautifulSoup(response.text, 'lxml')
        table_body = doc.select('div#files tbody')[0]

        # extract the file names
        file_names = [table_row.text for table_row in table_body.select('div[title]')]

        # extract each download link from table
        download_links = [table_row.get('href') for table_row in table_body.select('a.icon-download')]
        page_names_urls = list(zip(file_names, download_links))
        # print(page_names_urls)
        
        # download data
        print(f"downloading batch {page}...")
        download_data(page_names_urls)

    # url = "https://physionet.org/content/apnea-ecg/1.0.0/"
    # main_add = url.split(r'/content', 1)[0]
    # response = requests.get(url)

    # doc = BeautifulSoup(response.text, 'lxml')
    # table_body = doc.select('table.files-panel > tbody')[0]

    # page_names_urls = [
    #     # table_row.text
    #     (table_row.select_one('a').text, f"{main_add}{table_row.select_one('a[class="download"]').get('href')}") 
    #     for table_row in table_body.select('tr') if not table_row.get('class')
    # ]

    # https://physionet.org/files/apnea-ecg/1.0.0/ANNOTATORS?download
    # print(page_names_urls)

    # download_data(page_names_urls)

    
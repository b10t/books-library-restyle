import argparse
import os
from urllib.parse import unquote, urljoin, urlsplit

import requests
import urllib3
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib3.exceptions import InsecureRequestWarning

library_site_url = 'https://tululu.org/'
book_collection_url = 'http://tululu.org/l55/'

for page_number in range(1, 11):
    response = requests.get(f'{library_site_url}/l55/{page_number}/')
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'lxml')

    table_d_book = soup.find('div', id='content').select('table.d_book')

    for tag_a in table_d_book:
        print(urljoin(
            library_site_url,
            tag_a.find('a')['href']
        ))

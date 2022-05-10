import argparse
import os
import re
from itertools import count
from urllib.parse import unquote, urljoin, urlsplit

import requests
import urllib3
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib3.exceptions import InsecureRequestWarning

library_site_url = 'https://tululu.org/'
book_collection_url = 'http://tululu.org/l55/'


def check_for_redirect(response):
    """Проверка на редирект."""
    if response.history:
        raise requests.HTTPError


def get_book_ids_from_pages(library_site_url, start_page, end_page):
    """Получение ID книг из страниц."""
    for page_number in count(start_page):
        if page_number == end_page:
            return

        response = requests.get(f'{library_site_url}/l55/{page_number}/')
        response.raise_for_status()

        check_for_redirect(response)

        soup = BeautifulSoup(response.content, 'lxml')

        table_d_book = soup.select_one('div#content').select('table.d_book')

        for tag_a in table_d_book:
            book_href = tag_a.select_one('a').get('href')
            book_id = int(re.sub(r'[^0-9]', '', book_href))

            yield book_id


start_page = 700
end_page = 0

for book_id in get_book_ids_from_pages(library_site_url, start_page, end_page):
    print(book_id)

# for book_id in (x for x in count(700) if x != 702):
#     print(book_id)

# for page_number in range(1, 2):
#     response = requests.get(f'{library_site_url}/l55/{page_number}/')
#     response.raise_for_status()

#     soup = BeautifulSoup(response.content, 'lxml')

#     # table_d_book = soup.select_one('div#content').select('table.d_book')
#     table_d_book = soup.select_one('div#content').select('table.d_book')

#     for tag_a in table_d_book:
#         # print(urljoin(
#         #     library_site_url,
#         #     tag_a.find('a')['href']
#         # ))
#         print(int(re.sub(r'[^0-9]', '', tag_a.select_one('a').get('href'))))

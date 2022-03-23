import os
import re

import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


if __name__ == '__main__':
    urllib3.disable_warnings(InsecureRequestWarning)

    url = "https://tululu.org/txt.php"

    books_path = 'books'
    os.makedirs(books_path, exist_ok=True)

    for book_id in range(1, 11):

        params = {
            'id': book_id,
        }

        response = requests.get(url, verify=False, params=params)
        response.raise_for_status()

        try:
            check_for_redirect(response)
        except requests.HTTPError:
            continue

        filename = f'id{book_id}.txt'
        with open(os.path.join(books_path, filename), 'wb') as file:
            file.write(response.content)

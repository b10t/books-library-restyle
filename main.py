import os

import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

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

        filename = f'id{book_id}.txt'
        with open(os.path.join(books_path, filename), 'wb') as file:
            file.write(response.content)

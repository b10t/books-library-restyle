import os

import requests
import urllib3
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib3.exceptions import InsecureRequestWarning


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(url, filename, folder='books'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Ссылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    params = {
        'id': book_id,
    }

    response = requests.get(url, verify=False, params=params)
    response.raise_for_status()

    check_for_redirect(response)

    # filename = f'{book_id}. {book_author}.txt'
    with open(os.path.join(books_path, filename), 'wb') as file:
        file.write(response.content)


def get_book_description(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')

    title_tag = soup.find('h1')

    book_author, book_title = [text.strip()
                               for text in title_tag.text.split('::')]

    return book_author, book_title


if __name__ == '__main__':
    urllib3.disable_warnings(InsecureRequestWarning)

    url = "https://tululu.org/txt.php"

    books_path = 'books'
    os.makedirs(books_path, exist_ok=True)

    for book_id in range(1, 11):
        try:
            download_txt(url, book_id, books_path)
        except requests.HTTPError:
            continue

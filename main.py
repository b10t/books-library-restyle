import os
from urllib.parse import urlparse

import requests
import urllib3
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib3.exceptions import InsecureRequestWarning


def check_for_redirect(response):
    """Проверка на редирект."""
    if response.history and urlparse(response.url).path == '/':
        raise requests.HTTPError


def download_txt(url, filename, folder='books', params={}):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Ссылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    os.makedirs(folder, exist_ok=True)

    response = requests.get(url, verify=False, params=params)
    response.raise_for_status()

    check_for_redirect(response)

    book_save_path = os.path.join(folder, f'{sanitize_filename(filename)}.txt')
    with open(book_save_path, 'wb') as file:
        file.write(response.content)

    return book_save_path


def get_book_description(url):
    """Возвращает автора и название книги."""
    response = requests.get(url)
    response.raise_for_status()

    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'lxml')

    title_tag = soup.find('h1')

    book_title, book_author = [text.strip()
                               for text in title_tag.text.split('::')]

    return book_title, book_author


if __name__ == '__main__':
    urllib3.disable_warnings(InsecureRequestWarning)

    book_download_url = 'https://tululu.org/txt.php'
    book_description_url = 'https://tululu.org/b{}/'

    books_path = 'books'
    os.makedirs(books_path, exist_ok=True)

    for book_id in range(1, 11):
        params = {
            'id': book_id,
        }

        try:
            book_title, book_author = get_book_description(
                book_description_url.format(book_id)
            )

            download_txt(
                book_download_url,
                f'{book_id}. {book_title}',
                books_path,
                params)
        except requests.HTTPError:
            continue

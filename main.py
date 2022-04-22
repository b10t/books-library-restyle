import os
from urllib.parse import unquote, urljoin, urlparse, urlsplit

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
    """Функция для скачивания текстовых файлов."""
    os.makedirs(folder, exist_ok=True)

    response = requests.get(url, verify=False, params=params)
    response.raise_for_status()

    check_for_redirect(response)

    book_save_path = os.path.join(folder, f'{sanitize_filename(filename)}.txt')
    with open(book_save_path, 'wb') as file:
        file.write(response.content)

    return book_save_path


def download_image(url, folder='images'):
    """Скачивает изображение книги."""
    os.makedirs(folder, exist_ok=True)

    response = requests.get(url)
    response.raise_for_status()

    check_for_redirect(response)

    image_save_path = os.path.join(
        folder,
        os.path.basename(unquote(urlsplit(url).path))
    )

    with open(image_save_path, 'wb') as file:
        file.write(response.content)


def parse_book_page(page_content):
    """Возвращает данные страницы по книге."""
    soup = BeautifulSoup(page_content, 'lxml')

    title_tag = soup.find('h1')

    book_title, book_author = [text.strip()
                               for text in title_tag.text.split('::')]

    book_image_url = soup.find('div', class_='bookimage').find('img')['src']

    download_tag = soup.find('a', string='скачать txt')
    download_url = download_tag['href'] if download_tag else '/txt.php?id='

    comments = []

    for div in soup.select('div.texts'):
        for span in div.select('span.black'):
            comments.append(span.text)

    genres = []

    for span in soup.select('span.d_book'):
        for tag_a in span.select('a'):
            genres.append(tag_a.text)

    return dict(
        book_title=book_title,
        book_author=book_author,
        book_image_url=book_image_url,
        download_url=download_url,
        comments=comments,
        genres=genres)


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
            book_title, book_author, book_image_url = get_book_description(
                book_description_url.format(book_id)
            )

            download_txt(
                book_download_url,
                f'{book_id}. {book_title}',
                books_path,
                params)

            download_image(
                book_image_url
            )
        except requests.HTTPError:
            continue

import argparse
import json
import os
import pathlib
import re
from itertools import count
from urllib.parse import unquote, urljoin, urlsplit

import requests
import urllib3
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib3.exceptions import InsecureRequestWarning


def check_for_redirect(response):
    """Проверка на редирект."""
    if response.history:
        raise requests.HTTPError


def download_txt(url, filename, folder='books'):
    """Функция для скачивания текстовых файлов."""
    response = requests.get(url, verify=False)
    response.raise_for_status()

    check_for_redirect(response)

    book_save_path = os.path.join(folder, f'{sanitize_filename(filename)}.txt')
    with open(book_save_path, 'wb') as file:
        file.write(response.content)

    return book_save_path


def download_image(url, filename, folder='images'):
    """Скачивает изображение книги."""
    response = requests.get(url)
    response.raise_for_status()

    check_for_redirect(response)

    image_save_path = os.path.join(
        folder,
        filename
    )

    with open(image_save_path, 'wb') as file:
        file.write(response.content)


def parse_book_page(page_content):
    """Возвращает данные страницы по книге."""
    soup = BeautifulSoup(page_content, 'lxml')

    title_tag = soup.select_one('h1')

    book_title, book_author = [text.strip()
                               for text in title_tag.text.split('::')]

    book_image_url = soup.select_one('div.bookimage img')['src']

    download_tag = soup.find('a', string='скачать txt')
    download_tag = soup.find('a', string='скачать txt')
    download_url = download_tag['href'] if download_tag else '/txt.php'

    comments = [span.text for div in soup.select('div.texts')
                for span in div.select('span.black')]

    genres = [tag_a.text for span in soup.select('span.d_book')
              for tag_a in span.select('a')]

    return {
        'book_title': book_title,
        'book_author': book_author,
        'book_image_url': book_image_url,
        'download_url': download_url,
        'comments': comments,
        'genres': genres
    }


def get_book_ids_from_pages(library_site_url, start_page, end_page):
    """Получение ID книг из страниц."""
    for page_number in count(start_page):
        if page_number == end_page:
            return

        response = requests.get(f'{library_site_url}/l55/{page_number}/')
        response.raise_for_status()

        try:
            check_for_redirect(response)
        except requests.HTTPError:
            return

        soup = BeautifulSoup(response.content, 'lxml')

        table_d_book = soup.select_one('div#content').select('table.d_book')

        for tag_a in table_d_book:
            book_href = tag_a.select_one('a').get('href')
            book_id = int(re.sub(r'[^0-9]', '', book_href))

            yield book_id


def create_parser():
    parser = argparse.ArgumentParser(
        description='Скачивает книги с сайта tululu.org'
    )
    parser.add_argument('--start_page',
                        help='Начальный номер страницы',
                        type=int,
                        default=701,
                        nargs='?')

    parser.add_argument('--end_page',
                        help='Конечный номер страницы',
                        type=int,
                        default=0,
                        nargs='?')

    parser.add_argument('--dest_folder',
                        help='Путь к каталогу с результатами парсинга: картинкам, книгам, JSON',
                        type=pathlib.Path,
                        default='.')

    parser.add_argument('--skip_imgs',
                        help='Не скачивать картинки',
                        default='')

    parser.add_argument('--skip_txt',
                        help='Не скачивать книги',
                        default='')

    parser.add_argument('--json_path',
                        help='Указать свой путь к *.json файлу с результатами',
                        type=pathlib.Path,
                        default='books_descriptions.json')

    return parser.parse_args()


if __name__ == '__main__':
    urllib3.disable_warnings(InsecureRequestWarning)

    args = create_parser()

    books_folder = args.dest_folder / 'books'
    images_folder = args.dest_folder / 'images'
    json_path = args.dest_folder / args.json_path

    os.makedirs(books_folder, exist_ok=True)
    os.makedirs(images_folder, exist_ok=True)

    library_site_url = 'https://tululu.org/'

    books_descriptions = []

    for book_id in get_book_ids_from_pages(library_site_url, args.start_page, args.end_page):
        try:
            response = requests.get(f'{library_site_url}b{book_id}/')
            response.raise_for_status()

            check_for_redirect(response)

            book_description = parse_book_page(response.content)

            books_descriptions.append(book_description)

            book_url = urljoin(
                library_site_url,
                book_description['download_url']
            )
            book_filename = f'{book_id}. {book_description["book_title"]}'

            book_image_url = urljoin(
                library_site_url,
                book_description['book_image_url']
            )
            book_image_filename = os.path.basename(
                unquote(
                    urlsplit(book_image_url).path
                ))
            image_filename = f'{book_id}_{book_image_filename}'

            if not args.skip_txt:
                download_txt(book_url, book_filename, books_folder)

            if not args.skip_imgs:
                download_image(book_image_url, image_filename, images_folder)

            print(urljoin(
                library_site_url,
                f'b{book_id}'
            ))
        except requests.HTTPError or requests.ConnectionError:
            print('Не удалось скачать книгу с сервера.')

    with open(json_path, 'w', encoding='utf8') as json_file:
        json_file.write(json.dumps(books_descriptions, ensure_ascii=False))

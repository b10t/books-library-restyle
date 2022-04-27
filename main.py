import argparse
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

    title_tag = soup.find('h1')

    book_title, book_author = [text.strip()
                               for text in title_tag.text.split('::')]

    download_tag = soup.find('a', string='скачать txt')

    return {
        'book_title': book_title,
        'book_author': book_author,
        'book_image_url': soup.find('div', class_='bookimage').find('img')['src'],
        'download_url': download_tag['href'] if download_tag else '/txt.php?id=',
        'comments': [span.text for div in soup.select('div.texts')
                     for span in div.select('span.black')],
        'genres': [tag_a.text for span in soup.select('span.d_book')
                   for tag_a in span.select('a')]
    }


if __name__ == '__main__':
    os.makedirs('books', exist_ok=True)
    os.makedirs('images', exist_ok=True)

    urllib3.disable_warnings(InsecureRequestWarning)

    parser = argparse.ArgumentParser(
        description='Скачивает книги с сайта tululu.org'
    )
    parser.add_argument('start_id',
                        help='Начальный id книги',
                        type=int,
                        default=1)

    parser.add_argument('end_id',
                        help='Конечный id книги',
                        type=int,
                        default=10)

    args = parser.parse_args()

    url = 'https://tululu.org/'

    for book_id in range(args.start_id, args.end_id + 1):
        try:
            response = requests.get(f'{url}/b{book_id}')
            response.raise_for_status()

            check_for_redirect(response)

            page_content = parse_book_page(response.content)

            download_url = urljoin(url, page_content['download_url'])
            book_filename = f'{book_id}. {page_content["book_title"]}'

            book_image_url = urljoin(url, page_content['book_image_url'])
            image_filename = f'{book_id}_{os.path.basename(unquote(urlsplit(book_image_url).path))}'

            download_txt(download_url, book_filename)
            download_image(book_image_url, image_filename)
        except requests.ConnectionError:
            continue
        except requests.HTTPError:
            print('Не удалось скачать книгу с сервера.')
            continue

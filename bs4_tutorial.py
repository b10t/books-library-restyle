import os
from urllib.parse import urlparse

import requests
import urllib3
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib3.exceptions import InsecureRequestWarning


def check_for_redirect(response):
    if response.history and urlparse(response.url).path == '/':
        raise requests.HTTPError


def parse_book_page(page_content):
    """Возвращает данные страницы по книге."""
    soup = BeautifulSoup(page_content, 'lxml')

    title_tag = soup.find('h1')

    book_title, book_author = [text.strip()
                               for text in title_tag.text.split('::')]

    book_image_url = soup.find('div', class_='bookimage').find('img')['src']

    download_tag = soup.find('a', string='скачать txt')
    download_url = download_tag['href'] if download_tag else None

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


url = 'https://tululu.org/b9/'
response = requests.get(url)
response.raise_for_status()

print(parse_book_page(response.content))


# soup = BeautifulSoup(response.text, 'lxml')

# title_tag = soup.find('h1')

# book_author, book_title = [text.strip() for text in title_tag.text.split('::')]

# print(book_author, book_title)


# url = 'https://tululu.org/b7/'
# response = requests.get(url)
# response.raise_for_status()

# soup = BeautifulSoup(response.text, 'lxml')

# book_image_src = soup.find('div', class_='bookimage').find('img')['src']

# print(urljoin(url, book_image_src))

# url = 'https://tululu.org/b9/'
# response = requests.get(url)
# response.raise_for_status()

# soup = BeautifulSoup(response.text, 'lxml')

# download_tag = soup.find('a', string='скачать txt')
# download_url = download_tag['href'] if download_tag else None

# print(download_url)

# comments = soup.find_all('span', 'black').get_text
# comments = soup.find_all('div', 'texts').find_all('span')
# genres = []

# for span in soup.select('span.d_book'):
#     for tag_a in span.select('a'):
#         genres.append(tag_a.text)

# print(*genres, sep='\n')

# print(urljoin(url, book_image_src))
# print(*book_url)


# title_tag = soup.find('h1')

# book_author, book_title = [text.strip() for text in title_tag.text.split('::')]

# print(book_author, book_title)


# print(soup.find('img', class_='attachment-post-image')['src'])

# content = soup.find('main').find('div', class_='entry-content')

# tags = content.find_all('p')
# for tag in tags:
#     print(tag.text)

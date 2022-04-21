from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# url = 'https://tululu.org/b7/'
# response = requests.get(url)
# response.raise_for_status()

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


url = 'https://tululu.org/b9/'
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')

download_tag = soup.find('a', string='скачать txt')
download_url = download_tag['href'] if download_tag else None

print(download_url)

book_url = soup.find('table', class_='d_book').find_all('a')

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

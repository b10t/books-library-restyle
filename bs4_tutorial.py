import requests
from bs4 import BeautifulSoup


url = 'https://tululu.org/b7/'
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')

title_tag = soup.find('h1')

book_author, book_title = [text.strip() for text in title_tag.text.split('::')]

print(book_author, book_title)
# print(*[text.strip() for text in title_tag.text.split('::')], sep='\n')

# print(soup.find('img', class_='attachment-post-image')['src'])

# content = soup.find('main').find('div', class_='entry-content')

# tags = content.find_all('p')
# for tag in tags:
#     print(tag.text)

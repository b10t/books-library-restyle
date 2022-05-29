import json
import math
import os
import urllib.parse

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def on_reload():
    with open("books_catalog.json", "r") as books_file:
        books_json = books_file.read()

    books_catalog = json.loads(books_json)

    for book in books_catalog:
        book['image_filename'] = os.path.join(
            '/../images', book['image_filename'])
        book['book_filename'] = urllib.parse.quote(
            os.path.join('/../books', book['book_filename'])
        )

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    pages_number = math.ceil(len(books_catalog) / 20)

    for page_index, books in enumerate(chunked(books_catalog, 20)):
        page_save_path = os.path.join(
            'pages',
            f'index{page_index + 1}.html'
        )

        rendered_page = template.render(
            books_catalog=list(chunked(books, 2)),
            pages_number=pages_number + 1,
            page_index=page_index + 1,
        )

        with open(page_save_path, 'w', encoding="utf8") as file:
            file.write(rendered_page)


os.makedirs('pages', exist_ok=True)

on_reload()

server = Server()
server.watch('template.html', on_reload)
server.serve(root='.', default_filename='./pages/index1.html')

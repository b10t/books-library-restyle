from more_itertools import chunked
import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def on_reload():
    with open("books_catalog.json", "r") as books_file:
        books_json = books_file.read()

    books_catalog = json.loads(books_json)

    for book in books_catalog:
        book['image_filename'] = os.path.join('images', book['image_filename'])

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    rendered_page = template.render(
        books_catalog=list(chunked(books_catalog, 2)),
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


on_reload()

server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')

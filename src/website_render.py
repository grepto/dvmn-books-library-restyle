import json
from typing import List

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell


def get_books(books_json_file: str) -> List:
    with open(books_json_file, 'r') as books_json:
        books_json = books_json.read()

    books = json.loads(books_json)

    return books


def render_page(template_name: str, books: List, page_name: str, page_no: int, page_quantity: int):
    env = Environment(
        loader=FileSystemLoader('template'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template(template_name)
    page = template.render(books=books, page_no=page_no, page_quantity=page_quantity)

    with open(f'html/{page_name}', 'w', encoding='utf-8') as file:
        file.write(page)


def render_site():
    all_books = get_books('books.json')
    books_chunks = [all_books[x:x + 20] for x in range(0, len(all_books), 20)]

    for i, chunk in enumerate(books_chunks):
        render_page('index.html', chunk, f'index{i + 1}.html', i + 1, len(books_chunks))


if __name__ == '__main__':
    render_site()
    # server = Server()
    # server.watch('template/*.html', render_site)
    # server.serve(root='html/')

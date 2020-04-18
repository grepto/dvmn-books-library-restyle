import json
from typing import List

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
import more_itertools


def get_books(books_file_path: str) -> List:
    with open(books_file_path, 'r') as books_file:
        books_file = books_file.read()

    books = json.loads(books_file)

    return books


def render_page(template_folder: str, template_name: str, destination_folder: str, books: List, page_name: str, page_no: int, page_quantity: int):
    env = Environment(
        loader=FileSystemLoader(template_folder),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template(template_name)
    page = template.render(books=books, page_no=page_no, page_quantity=page_quantity)

    with open(f'{destination_folder}/{page_name}', 'w', encoding='utf-8') as file:
        file.write(page)


def render_site(template_folder: str,
                template_name: str,
                destination_folder: str,
                json_file: str,
                books_per_page: int):
    all_books = get_books(json_file)
    books_chunks = list(more_itertools.chunked(all_books, books_per_page))

    for page_no, chunk in enumerate(books_chunks, 1):
        render_page(template_folder=template_folder,
                    template_name=template_name,
                    destination_folder=destination_folder,
                    books=chunk,
                    page_name=f'index{page_no}.html',
                    page_no=page_no,
                    page_quantity=len(books_chunks),
                    )


def start_server():
    render_site()
    server = Server()
    server.watch('template/*.html', render_site)
    server.serve(root='html/')


if __name__ == '__main__':
    render_site()

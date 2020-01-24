import json

from book import download_book
from category import get_books_urls


def batch_download(book_limit: int):
    urls = get_books_urls(book_limit)
    books_contexts = [download_book(url) for url in urls]

    return books_contexts


def main(book_limit: int):
    books = batch_download(book_limit)

    with open('books.json', 'w') as json_file:
        json.dump(books, json_file, ensure_ascii=False)


if __name__ == '__main__':
    main(10)

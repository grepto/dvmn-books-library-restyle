import argparse
import json
from typing import List, Optional

from book import download_book
from category import get_books_urls
import config


def batch_download(start_page: int, end_page: Optional[int] = None) -> List:
    urls = get_books_urls(start_page, end_page)
    books_contexts = []

    for url in urls:
        book_context = download_book(url)
        books_contexts.append(book_context) if book_context else None

    return books_contexts


def create_parser():
    parser = argparse.ArgumentParser(description='Book downloader')

    parser.add_argument('--start_page', type=int, help='From page')
    parser.add_argument('--end_page', type=int, default=0, help='To page (exclude)')

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    books = batch_download(args.start_page, args.end_page)

    with open(config.BOOK_JSON_FILE, 'w') as json_file:
        json.dump(books, json_file, ensure_ascii=False)


if __name__ == '__main__':
    main()

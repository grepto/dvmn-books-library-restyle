import argparse
import json
from typing import List

from tqdm import tqdm

from book import download_book
from category import get_books_urls


def batch_download(start_page: int, end_page: int, book_path: str, image_path: str, category_url: str) -> List:
    urls = tqdm(get_books_urls(start_page, end_page, category_url))
    books_contexts = []

    for url in urls:
        urls.set_description(f'Downloading {url}')
        book_context = download_book(url, book_path, image_path)
        books_contexts.append(book_context) if book_context else None

    return books_contexts


def create_parser():
    parser = argparse.ArgumentParser(description='Book downloader')

    parser.add_argument('--start_page', type=int, help='From page')
    parser.add_argument('--end_page', type=int, default=0, help='To page (exclude)')
    parser.add_argument('--book_path', type=str, default='books', help='Path to store book files')
    parser.add_argument('--image_path', type=str, default='images', help='Path to store book covers image files')
    parser.add_argument('--category_url', type=str, default='http://tululu.org/l55/', help='Book category url')
    parser.add_argument('--book_json', type=str, default='books.json', help='Name of destination json file')

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    books = batch_download(args.start_page, args.end_page, args.book_path, args.image_path, args.category_url)

    with open(args.book_json, 'w') as json_file:
        json.dump(books, json_file, ensure_ascii=False)


if __name__ == '__main__':
    main()

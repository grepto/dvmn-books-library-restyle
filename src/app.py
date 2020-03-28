import argparse
import json

import defaults
from book import download_books
from website_render import render_site


def create_parser():
    parser = argparse.ArgumentParser(description='Book downloader')

    parser.add_argument('--start_page', type=int, help='From page')
    parser.add_argument('--end_page', type=int, default=defaults.END_PAGE, help='To page (exclude)')
    parser.add_argument('--root_path', type=str, default=defaults.ROOT_PATH, help='Root path to store content')
    parser.add_argument('--book_path', type=str, default=defaults.BOOK_PATH, help='Path to store book files')
    parser.add_argument('--image_path', type=str, default=defaults.IMAGE_PATH, help='Path to store book covers image files')
    parser.add_argument('--category_url', type=str, default=defaults.CATEGORY_URL, help='Book category url')
    parser.add_argument('--book_json', type=str, default=defaults.JSON_FILE, help='Name of destination json file')
    parser.add_argument('--html_template_path', type=str, default=defaults.TEMPLATE_PATH, help='Path to html templates')
    parser.add_argument('--html_template', type=str, default=defaults.TEMPLATE_NAME, help='Name of html template file')
    parser.add_argument('--books_per_page', type=int, default=defaults.BOOKS_PER_PAGE, help='Quantity of books per one page')

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    books = download_books(args.start_page,
                           args.end_page,
                           args.book_path,
                           args.image_path,
                           args.category_url,
                           )

    with open(args.book_json, 'w') as json_file:
        json.dump(books, json_file, ensure_ascii=False)

    render_site(template_folder=args.html_template_path,
                template_name=args.html_template,
                destination_folder=args.root_path,
                json_file=args.book_json,
                books_per_page=args.books_per_page,
                )


if __name__ == '__main__':
    main()

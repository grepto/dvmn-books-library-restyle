import re
from typing import Union, Tuple
import os

import requests
from pathvalidate import sanitize_filename


class NotTextBookError(Exception):
    pass


def get_file_name_by_content_disposition(cd: str) -> Union[str, None]:
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    file_name = re.findall('filename="(.+)"', cd)
    if len(file_name) == 0:
        return None
    return file_name[0]


def get_book_content(url: str) -> Tuple[str, bytes]:
    response_headers = requests.head(url)

    content_type = response_headers.headers.get('Content-Type')

    if 'text/plain' not in content_type:
        raise NotTextBookError

    response = requests.get(url=url)
    response.raise_for_status()

    cd = response.headers.get('content-disposition')
    file_name = get_file_name_by_content_disposition(cd=cd)

    return file_name, response.content


def save_book(book: bytes, name: str, path: str = None) -> str:
    if path:
        os.makedirs(path, exist_ok=True)

    file_name = os.path.join(path, sanitize_filename(name))

    with open(file_name, 'wb') as book_file:
        book_file.write(book)

    return file_name


if __name__ == '__main__':
    url = 'http://tululu.org/txt.php?id=32168'
    download_book_by_url(url=url)

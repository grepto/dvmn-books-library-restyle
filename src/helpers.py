import os
from urllib.parse import urljoin

from pathvalidate import sanitize_filename

BASE_URL = 'http://tululu.org/'


def get_absolute_url(relative_url: str) -> str:
    return urljoin(BASE_URL, relative_url)


def save_file(content: bytes, name: str, path: str = None) -> str:
    if path:
        os.makedirs(path, exist_ok=True)

    file_name = os.path.join(path, sanitize_filename(name))

    with open(file_name, 'wb') as file:
        file.write(content)

    return file_name

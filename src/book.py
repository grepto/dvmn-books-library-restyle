import re
from typing import Union

import requests


def get_file_name_by_content_disposition(cd: str) -> Union[str, None]:
    """
    Get filename from content-disposition
    """
    file_name = re.findall('filename="(.+)"', cd)
    if len(file_name) == 0:
        return None
    return file_name[0]


def download_book_by_url(url: str) -> None:
    response = requests.get(url=url)
    response.raise_for_status()

    cd = response.headers.get('content-disposition')
    file_name = get_file_name_by_content_disposition(cd=cd)

    with open(file_name, 'wb') as book:
        book.write(response.content)


if __name__ == '__main__':
    url = 'http://tululu.org/txt.php?id=32168'
    download_book_by_url(url=url)

import re
from typing import Dict, List, Tuple, Union

import requests
from bs4 import BeautifulSoup

from config import BOOK_FILE_PATH, IMAGE_FILE_PATH
from helpers import get_absolute_url, save_file


class NotTextBookError(Exception):
    pass


class NoFileAvaliable(Exception):
    pass


def get_book_file_name_by_content_disposition(cd: str) -> Union[str, None]:
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
    file_name = get_book_file_name_by_content_disposition(cd=cd)

    return file_name, response.content


def get_image_content(url: str) -> Tuple[str, bytes]:
    response = requests.get(url=url)
    response.raise_for_status()

    file_name = url.split('/')[-1]

    return file_name, response.content


def get_book_file_url(soup) -> str:
    tag = soup.select_one('table.d_book a[href*="/txt"]')

    if not tag:
        raise NoFileAvaliable

    relative_url = tag['href']
    return get_absolute_url(relative_url)


def get_book_genres(soup) -> List[str]:
    return [tag.text for tag in soup.select('span.d_book a')]


def get_book_comments(soup) -> List[str]:
    return [tag.text for tag in soup.select('.texts span')]


def get_book_title_and_author(soup) -> Tuple[str, str]:
    title_and_author = soup.select_one('h1').text.split('::')
    title, author = [item.strip() for item in title_and_author]
    return title, author


def get_book_image_url(soup) -> str:
    relative_url = soup.select_one('.bookimage a img')['src']

    return get_absolute_url(relative_url)


def get_book_context(book_page_url: str) -> Dict:
    response = requests.get(book_page_url)
    soup = BeautifulSoup(response.text, 'lxml')
    book_file_download_url = get_book_file_url(soup)
    return dict(
        title=get_book_title_and_author(soup)[0],
        author=get_book_title_and_author(soup)[1],
        comments=get_book_comments(soup),
        genres=get_book_genres(soup),
        book_file_download_url=book_file_download_url,
        book_image_download_url=get_book_image_url(soup),
    )


def download_book(book_page_url: str) -> Dict:
    try:
        book_context = get_book_context(book_page_url)
    except NoFileAvaliable:
        return None

    book_file_name, book_content = get_book_content(book_context.get('book_file_download_url'))

    book_local_file_name = save_file(book_content, book_file_name, BOOK_FILE_PATH)

    image_file_name, image_content = get_image_content(book_context.get('book_image_download_url'))
    image_local_file_name = save_file(image_content, image_file_name, IMAGE_FILE_PATH)

    book_context.update(
        book_path=book_local_file_name,
        img_src=image_local_file_name,
    )

    return book_context

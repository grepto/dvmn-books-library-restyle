from math import ceil
from typing import List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from config import CATEGORY_URL
from helpers import get_absolute_url

BOOKS_PER_PAGE = 25


def get_pages_urls(limit: int = 0) -> List[str]:
    response = requests.get(CATEGORY_URL)
    soup = BeautifulSoup(response.text, 'lxml')

    if not limit:
        limit = soup.select_one('#content .center a:last-child').text

    return [urljoin(CATEGORY_URL, str(page_id)) for page_id in range(1, limit + 1)]


def get_book_urls_from_page(page_url: str) -> List[str]:
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'lxml')

    return [get_absolute_url(tag['href']) for tag in soup.select('.bookimage a')]


def get_books_urls(limit: int = 0) -> List[str]:
    pages_limit = ceil(limit / BOOKS_PER_PAGE)
    links = []

    for page_url in get_pages_urls(limit=pages_limit):
        links.extend(get_book_urls_from_page(page_url))

    return links[:limit]

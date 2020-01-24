from typing import List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from config import CATEGORY_URL
from helpers import get_absolute_url

BOOKS_PER_PAGE = 25


def get_last_category_page_id() -> int:
    response = requests.get(CATEGORY_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    last_category_page_id = soup.select_one('#content .center a:last-child').text
    return int(last_category_page_id)


def get_book_urls_from_page(page_url: str) -> List[str]:
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'lxml')

    return [get_absolute_url(tag['href']) for tag in soup.select('.bookimage a')]


def get_books_urls(start_page: int, end_page: Optional[int] = None) -> List[str]:
    end_page = end_page or get_last_category_page_id() + 1

    links = []
    for id in range(start_page, end_page):
        links.extend(get_book_urls_from_page(urljoin(CATEGORY_URL, str(id))))

    return links

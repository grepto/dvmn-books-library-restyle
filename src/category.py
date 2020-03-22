from typing import List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from helpers import get_absolute_url

BOOKS_PER_PAGE = 25


def get_last_category_page_id(category_url: str) -> int:
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, 'lxml')
    last_category_page_id = soup.select_one('#content .center a:last-child').text
    return int(last_category_page_id)


def get_book_urls_from_page(page_url: str) -> List[str]:
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'lxml')

    return [get_absolute_url(tag['href']) for tag in soup.select('.bookimage a')]


def get_books_urls(start_page: int, end_page: int, category_url: str) -> List[str]:
    end_page = end_page or get_last_category_page_id(category_url) + 1

    links = []
    for id in range(start_page, end_page):
        links.extend(get_book_urls_from_page(urljoin(category_url, str(id))))

    return links

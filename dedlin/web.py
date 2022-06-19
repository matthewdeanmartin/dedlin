from typing import Generator

import requests


def fetch_page_as_rows(url: str) -> Generator[str, None, None]:
    """Fetch a page as a list of rows"""
    response = requests.get(url)
    for line in response.text.splitlines():
        yield line

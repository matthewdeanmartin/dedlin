"""
Fetch lines from web, assuming html, turn into text
"""

import html2text
import requests


def fetch_page_as_rows(url: str) -> str:
    """Fetch a page as a list of rows"""
    # TODO: handle popular line based formats, e.g. CVS
    response = requests.get(url)
    h = html2text.HTML2Text()
    h.ignore_links = True
    return h.handle(response.text)

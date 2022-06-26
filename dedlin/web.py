"""
Fetch lines from web, assuming html, turn into text
"""
import html2text
import requests


def fetch_page_as_rows(url: str) -> list[str]:
    """Fetch a page as a list_doc of rows"""
    # TODO: handle popular line based formats, e.g. CVS
    response = requests.get(url)
    handler = html2text.HTML2Text()
    handler.ignore_links = True
    text = handler.handle(response.text)
    while "\n\n" in text:
        text = text.replace("\n\n", "\n")
    lines = [_.strip() for _ in text.split("\n")]
    while lines[-1].strip() == "":
        lines.pop()
    return lines


if __name__ == "__main__":
    fetch_page_as_rows("https://www.google.com")

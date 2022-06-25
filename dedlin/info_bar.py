"""
An info bar that runs after each command, replaces bottom bar in a full screen editor
"""
from typing import Generator

from dedlin.document import Document


def display_info(document: Document) -> Generator[tuple[str, str], None, None]:
    all_text = "".join(document.lines)
    yield "okay, yo", "\n"

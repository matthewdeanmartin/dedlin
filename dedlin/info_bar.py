"""
An info bar that runs after each command, replaces bottom bar in a full screen editor
"""
from typing import Generator

from textstat import textstat

from dedlin.document import Document


def display_info(document: Document) -> Generator[tuple[str, str], None, None]:
    """Display some natural language statistics about the document"""
    text = "".join(document.lines)
    time_to_read = textstat.reading_time(text, ms_per_char=14.69)
    yield f"{time_to_read} minutes to read", "\n"
    words = textstat.lexicon_count(text, removepunct=True)
    yield f"{words} words", "\n"
    sentences = textstat.sentence_count(text)
    yield f"{sentences} sentences", "\n"
    characters = textstat.char_count(text, ignore_spaces=True)
    yield f"{characters} characters", "\n"

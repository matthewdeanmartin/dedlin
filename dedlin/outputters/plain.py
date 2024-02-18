"""
Abstraction over print-to-standard-out.
"""

from typing import Optional


def plain_printer(text: Optional[str], end: str = "\n") -> None:
    """Print text to standard out.

    Args:
        text (Optional[str]): The text to print
        end (str): The end. Defaults to "\n".
    """
    text = "" if text is None else text
    if text.endswith("\n"):
        text = text[:-1]
        print(text, end="")
    else:
        print(text, end=end)

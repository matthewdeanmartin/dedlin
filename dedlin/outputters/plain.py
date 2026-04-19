"""
Abstraction over print-to-standard-out.
"""

from typing import Optional


def plain_printer(text: Optional[str], end: str = "\n", start_line: int = 0) -> None:
    """Print text to standard out.

    Args:
        text (Optional[str]): The text to print
        end (str): The end. Defaults to "\n".
        start_line (int): The line number. Defaults to 0.
    """
    text = "" if text is None else text
    if start_line > 0:
        text = f"   {start_line} : {text}"
    if text.endswith("\n"):
        text = text[:-1]
        print(text, end="")
    else:
        print(text, end=end)

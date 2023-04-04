from typing import Optional


def plain_printer(text: Optional[str], end: str = "\n") -> None:
    text = "" if text is None else text
    if text.endswith("\n"):
        text = text[:-1]
        print(text, end="")
    else:
        print(text, end=end)
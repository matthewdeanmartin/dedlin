"""Make the output of the program more readable."""
from typing import Optional

from rich.console import Console
from rich.syntax import Syntax


class RichPrinter:
    """Make the output of the program more readable."""

    def __init__(self) -> None:
        """Set up initial state"""
        self.console = Console()

    def print(self, text: str, end: Optional[str]) -> None:
        """Syntax highlighting

        Args:
            text (str): The text to print
            end (Optional[str]): The end
        """
        text = "" if text is None else text
        if text and text.endswith("\n"):
            text = text[:-1]
        syntax = Syntax(
            text,
            "python",
            # theme="monokai",
            line_numbers=False,
        )
        self.console.print(syntax, end=end)


rich_printer = RichPrinter()


def printer(text: Optional[str], end: str = "\n") -> None:
    """Print text to standard out.

    Args:
        text (Optional[str]): The text to print
        end (str): The end. Defaults to "\n".
    """
    text = "" if text is None else text
    rich_printer.print(text, end="")

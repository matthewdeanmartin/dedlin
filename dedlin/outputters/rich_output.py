"""Make the output of the program more readable."""

from typing import Optional

from rich.console import Console
from rich.syntax import Syntax


class RichPrinter:
    """Make the output of the program more readable."""

    def __init__(self) -> None:
        """Set up initial state"""
        self.console = Console()

    def print(self, text: str, end: Optional[str], start_line: int = 0) -> None:
        """Syntax highlighting

        Args:
            text (str): The text to print
            end (Optional[str]): The end
            start_line (int): The start line for numbering. Defaults to 0.
        """
        if not end:
            end = ""
        text = "" if text is None else text
        if text and text.endswith("\n"):
            text = text[:-1]

        if start_line > 0:
            syntax = Syntax(
                text,
                "python",
                # theme="monokai",
                line_numbers=True,
                start_line=start_line,
            )
            self.console.print(syntax, end=end)
        else:
            self.console.print(text, end=end)


rich_printer = RichPrinter()


# pylint: disable=unused-argument
def printer(text: Optional[str], end: str = "\n", start_line: int = 0) -> None:
    """Print text to standard out.

    Args:
        text (Optional[str]): The text to print
        end (str): The end. Defaults to "\n".
        start_line (int): The start line. Defaults to 0.
    """
    text = "" if text is None else text
    rich_printer.print(text, end="", start_line=start_line)

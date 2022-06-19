"""Make the output of the program more readable."""
from typing import Optional

from rich.console import Console
from rich.syntax import Syntax


class RichPrinter:
    """ "Make the output of the program more readable."""

    def __init__(self) -> None:
        """Set up initial state"""
        self.console = Console()

    def print(self, text, end: Optional[str]) -> None:
        """Syntax highlighting"""
        if text and text.endswith("\n"):
            text = text[:-1]
        syntax = Syntax(text, "python", theme="monokai", line_numbers=False)
        self.console.print(syntax, end=end)

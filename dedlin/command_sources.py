"""
Interactive command input methods.

These handle history, syntax highlighting, and auto-suggestion.
"""
from pathlib import Path
from typing import Generator, Iterable, Optional

import questionary
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.styles import get_style_by_name

from dedlin.basic_types import Command
from dedlin.parsers import parse_command
from dedlin.pygments_code import EdLexer

# from prompt_toolkit.shortcuts import prompt
# from pygments.lexers import guess_lexer_for_filename
# from prompt_toolkit.completion import Completer, Completion
# from prompt_toolkit.formatted_text import HTML

# thing = guess_lexer_for_filename("cats.py","")
style = style_from_pygments_cls(get_style_by_name("borland"))


SESSION: Optional[PromptSession] = None


class InteractiveGenerator:
    """Get a typed command from the user"""

    def __init__(self) -> None:
        """Initialize the generator"""
        self.current_line: int = 0
        self.document_length: int = 0
        self.prompt: str = "> "

    def generate(
        self,
    ) -> Generator[Command, None, None]:
        """Wrapper around prompt_toolkit for command input but typed"""
        user_command_text = ""
        while user_command_text is not None:
            user_command_text = next(_interactive_command_handler(self.prompt))
            command = parse_command(
                user_command_text, current_line=self.current_line, document_length=self.document_length
            )
            yield command


def _interactive_command_handler(prompt: str = "*") -> Generator[str, None, None]:
    """Wrapper around prompt_toolkit for command input"""
    # pylint: disable=global-statement
    global SESSION
    if SESSION is None:
        SESSION = PromptSession(
            history=InMemoryHistory(),
        )
    while True:
        text = SESSION.prompt(
            prompt,
            lexer=PygmentsLexer(EdLexer),
            style=style,
            default="",
            include_default_pygments_style=False,
            enable_history_search=True,
            auto_suggest=AutoSuggestFromHistory(),
        )
        yield text


def questionary_command_handler(prompt: str = "*") -> Generator[str, None, None]:
    """Wrapper around questionary for command input"""
    # possibly should merge with simple_input?
    while True:
        answer = questionary.text(prompt).ask()
        yield answer


class CommandGenerator:
    """Get a typed command from a file"""

    def __init__(self, path: Path):
        """Initialize the generator"""
        self.current_line: int = 0
        self.document_length: int = 0
        self.macro_path: Path = path
        self.prompt: str = "> "

    def generate(
        self,
    ) -> Generator[Command, None, None]:
        """Turn a file into a bunch of commands"""

        with open(str(self.macro_path), encoding="utf-8") as file:
            for line in file:
                command = parse_command(
                    line.strip("\n").strip("\r"), current_line=self.current_line, document_length=self.document_length
                )
                yield command


class InMemoryCommandGenerator:
    """A bunch of predefined commands"""

    def __init__(self, commands: Iterable[Command]):
        """Initialize the generator"""
        self.current_line: int = 0
        self.document_length: int = 0
        self.commands: Iterable[Command] = commands

    def generate(
        self,
    ) -> Generator[Command, None, None]:
        """Return a predefined command"""
        yield from self.commands


if __name__ == "__main__":
    print("This is a module, not a program.")

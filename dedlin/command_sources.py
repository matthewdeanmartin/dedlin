"""
Interactive command input methods.

These handle history, syntax highlighting, and auto-suggestion.
"""
from pathlib import Path
from typing import Generator

import questionary
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.styles import get_style_by_name

from dedlin.pygments_code import EdLexer

# from prompt_toolkit.shortcuts import prompt
# from pygments.lexers import guess_lexer_for_filename
# from prompt_toolkit.completion import Completer, Completion
# from prompt_toolkit.formatted_text import HTML

# thing = guess_lexer_for_filename("cats.py","")
style = style_from_pygments_cls(get_style_by_name("monokai"))

SESSION = None


def interactive_command_handler(prompt: str = "*") -> Generator[str, None, None]:
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


def command_generator(macro_path: Path) -> Generator[str, None, None]:
    """Turn a file into a bunch of commands"""
    with open(str(macro_path), encoding="utf-8") as file:
        yield from file

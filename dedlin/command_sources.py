from pathlib import Path
from typing import Generator

import questionary


def interactive_command_handler(prompt: str = "*") -> Generator[str, None, None]:
    """Wrapper around questionary for command input"""
    # possibly should merge with simple_input?
    while True:
        answer = questionary.text(prompt).ask()
        yield answer


def command_generator(macro_path: Path) -> Generator[str, None, None]:
    """Turn a file into a bunch of commands"""
    with open(str(macro_path), encoding="utf-8") as file:
        yield from file

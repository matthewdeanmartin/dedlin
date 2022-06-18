"""
Basic classes and mypy types
"""
import logging
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Generator, Optional, Protocol

logger = logging.getLogger(__name__)


class Commands(Enum):
    """Enum of commands that can be executed on a document."""

    Empty = auto()
    List = auto()
    Page = auto()
    Quit = auto()
    Exit = auto()
    Save = auto()
    Insert = auto()
    Edit = auto()
    Delete = auto()
    Help = auto()
    Lorem = auto()
    Undo = auto()
    Unknown = auto()
    Shuffle = auto()
    Sort = auto()
    Reverse = auto()
    Search = auto()
    Replace = auto()


@dataclass(frozen=True)
class LineRange:
    """A 1-base range of lines"""

    start: int
    end: int
    repeat: int = 1

    def count(self):
        """How many rows on a 1-based index"""
        return self.end - self.start + 1

    def validate(self):
        """Check if ranges are sensible"""
        validate = 1 <= self.start <= self.end and self.end >= 1
        if not validate:
            logger.warning(f"Invalid line range: {self}")
        return validate


@dataclass(frozen=True)
class Phrases:
    """End part of a command, especially for search/replace"""

    first: str
    second: str = ""
    third: str = ""
    fourth: str = ""
    fifth: str = ""


@dataclass(frozen=True)
class Command:
    """One parse structure for almost all commands."""

    command: Commands
    line_range: Optional[LineRange] = None
    phrases: Optional[Phrases] = None
    original_text: Optional[str] = field(default=None, compare=False)


def command_generator(macro_path: Path) -> Generator[str, None, None]:
    """Turn a file into a bunch of commands"""
    with open(str(macro_path), "r", encoding="utf-8") as file:
        for line in file:
            yield line


class Printable(Protocol):
    """Something that acts like print()"""

    def __call__(self, text: Optional[str], end: str = "\n") -> None:
        ...

"""
Basic classes and mypy types
"""
import logging
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Protocol

logger = logging.getLogger(__name__)


# noinspection PyArgumentList
class Commands(Enum):
    """Enum of commands that can be executed on a document."""

    EMPTY = auto()
    # display
    LIST = auto()
    PAGE = auto()
    SEARCH = auto()

    # edit commands
    INSERT = auto()
    EDIT = auto()
    LOREM = auto()
    DELETE = auto()
    REPLACE = auto()

    # file and exit
    QUIT = auto()
    EXIT = auto()
    TRANSFER = auto()
    BROWSE = auto()

    # reorder commands
    MOVE = auto()
    COPY = auto()
    SHUFFLE = auto()
    SORT = auto()
    REVERSE = auto()

    # Commands and Macros
    HISTORY = auto()
    REDO = auto()
    MACRO = auto()

    # other
    HELP = auto()
    UNDO = auto()
    UNKNOWN = auto()


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

    def validate(self):
        """Check if ranges are sensible"""
        if self.line_range:
            line_range_is_valid = self.line_range.validate()
            if not line_range_is_valid:
                return False
        return True


def try_parse_int(value) -> Optional[int]:
    """ "Parse int without raising errors"""
    try:
        return int(value)
    except ValueError:
        return None


class Printable(Protocol):
    """Something that acts like print()"""

    def __call__(self, text: Optional[str], end: str = "\n") -> None:
        ...

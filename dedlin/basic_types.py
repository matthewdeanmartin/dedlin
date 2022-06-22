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

    def format(self):
        if self.start == self.end and self.repeat == 1:
            range_part = str(self.start)
        else:
            range_part = f"{self.start},{self.end}"

        repeat_part = f",{self.repeat}" if self.repeat != 1 else ""
        return range_part + repeat_part

@dataclass(frozen=True)
class Phrases:
    """End part of a command, especially for search/replace"""

    first: str
    second: str = ""
    third: str = ""
    fourth: str = ""
    fifth: str = ""

    def format(self):
        """Round tripable format"""
        parts = [self.first, self.second, self.third, self.fourth, self.fifth]
        usable_parts =[]
        def safe_quote(value:str)->str:
            """Escape spaces and double quotes"""
            if " " in value and '"' not in value:
                return f'"{value}"'
            if " " in value and '"' in value:
                value = value.replace('"','\\"')
                return f'"{value}'
            return value

        for part in parts:
            if part:
                usable_parts.append(part)
            else:
                break

        return " ".join(safe_quote(_) for _ in parts if _)


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

    def format(self):
        range_part = self.line_range.format() if self.line_range is not None else ""
        phrase_part = self.phrases.format() if self.phrases is not None else ""
        return " ".join([range_part, self.command.name, phrase_part])


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

"""
Basic classes and mypy types
"""

import dataclasses
import logging
from enum import Enum, auto
from typing import Generator, Optional, Protocol, runtime_checkable

from pydantic import field_validator
from pydantic.dataclasses import dataclass

logger = logging.getLogger(__name__)


# noinspection PyArgumentList
class Commands(Enum):
    """Enum of commands that can be executed on a document."""

    COMMENT = auto()
    EMPTY = auto()
    NOOP = auto()  # ed compatibility
    # display
    LIST = auto()
    PAGE = auto()
    SEARCH = auto()
    SPELL = auto()
    CURRENT = auto()

    # edit commands
    INSERT = auto()
    PUSH = auto()
    EDIT = auto()
    LOREM = auto()
    DELETE = auto()
    REPLACE = auto()

    # file and exit
    WRITE = auto()  # Alis for EXIT
    SAVE = auto()  # Alias for EXIT
    QUIT = auto()
    EXIT = auto()
    TRANSFER = auto()
    EXPORT = auto()

    # Add text
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
    INFO = auto()
    CRASH = auto()

    # print
    PRINT = auto()

    # Block String commands
    INDENT = auto()
    DEDENT = auto()

    # String commands
    TITLE = auto()
    SWAPCASE = auto()
    CASEFOLD = auto()
    CAPITALIZE = auto()
    UPPER = auto()
    LOWER = auto()
    EXPANDTABS = auto()
    RJUST = auto()
    LJUST = auto()
    CENTER = auto()
    RSTRIP = auto()
    LSTRIP = auto()
    STRIP = auto()


@dataclass(frozen=True)
class LineRange:
    """A 1-base range of lines

    TODO: refactor to start + positive offset and end is a convenience property
    """

    start: int
    offset: int
    repeat: int = 1

    # problem when doc is 0 lines long
    @field_validator("start")
    @classmethod
    def start_must_be_one_or_more(cls, start: int) -> int:
        """Start must be 1 or more
        Args:
            start (int): The start value
        Returns:
            int: The start value
        """
        if start < 1:
            raise ValueError("start must be one or more")
        return start

    @field_validator("offset")
    @classmethod
    def offset_zero_or_more(cls, offset: int) -> int:
        """Offset must be zero or more

        Returns:
            int: The offset value
        """
        if offset < 0:
            raise ValueError("offset must be zero or more")
        return offset

    @field_validator("repeat")
    @classmethod
    def repeat_zero_or_more(cls, repeat: int) -> int:
        """Repeat must be zero or more

        Args:
            repeat (int): The repeat value

        Returns:
            int: The repeat value
        """
        if repeat < 0:
            raise ValueError("repeat must be zero or more")
        return repeat

    @property
    def end(self) -> int:
        """Make this derived so that start and end are valid as long as they are positive

        Returns:
            int: The end of the range
        """
        return self.start + self.offset

    def count(self) -> int:
        """How many rows on a 1-based index.

        Returns:
            int: The number of rows
        """
        return self.end - self.start + 1

    def validate(self) -> bool:
        """Check if ranges are sensible

        Returns:
            bool: True if ranges are sensible
        """
        validate = 1 <= self.start <= self.end and self.end >= 1 and self.repeat >= 0
        if not validate:
            logger.warning(f"Invalid line range: {self}")
        return validate

    def to_slice(self) -> slice:
        """Convert to a slice

        Returns:
            slice: The slice
        """
        return slice(self.start - 1, self.end)

    def format(self) -> str:
        """Format the range as a string

        Returns:
            str: The formatted range
        """
        if self.start == self.end and self.repeat == 1:
            range_part = str(self.start)
        else:
            range_part = f"{self.start},{self.end}"

        repeat_part = f",{self.repeat}" if self.repeat != 1 else ""
        return range_part + repeat_part


# can't freeze anymore because of list.
@dataclass(frozen=True)
class Phrases:
    """End part of a command, especially for search/replace

    TODO: refactor as list with convenience properties named first, second, etc.
    """

    # TODO: refactor to tuple so we can freeze this.
    parts: tuple[str, ...] = dataclasses.field(default_factory=lambda: ())

    @property
    def first(self) -> Optional[str]:
        """First phrase

        Returns:
            Optional[str]: The first phrase
        """
        return self.parts[0] if len(self.parts) > 0 else None

    @property
    def second(self) -> Optional[str]:
        """Return the second phrase

        Returns:
            Optional[str]: The second phrase
        """
        return self.parts[1] if len(self.parts) > 1 else None

    @property
    def third(self) -> Optional[str]:
        """Return the third part of the phrases

        Returns:
            Optional[str]: The third phrase
        """
        return self.parts[2] if len(self.parts) > 2 else None

    @property
    def fourth(self) -> Optional[str]:
        """Return the fourth phrase
        Returns:
            Optional[str]: The fourth phrase
        """
        return self.parts[3] if len(self.parts) > 3 else None

    @property
    def fifth(self) -> Optional[str]:
        """Return the fifth phrase

        Returns:
            Optional[str]: The fifth phrase
        """
        return self.parts[4] if len(self.parts) > 4 else None

    @property
    def sixth(self) -> Optional[str]:
        """Return the sixth part of the phrases

        Returns:
            Optional[str]: The sixth phrase
        """
        return self.parts[5] if len(self.parts) > 5 else None

    @property
    def seventh(self) -> Optional[str]:
        """Return the seventh phrase

        Returns:
            Optional[str]: The seventh phrase
        """
        return self.parts[6] if len(self.parts) > 6 else None

    @property
    def eighth(self) -> Optional[str]:
        """Return the eighth phrase

        Returns:
            Optional[str]: The eighth phrase
        """
        return self.parts[7] if len(self.parts) > 7 else None

    @property
    def ninth(self) -> Optional[str]:
        """Return the ninth phrase
        Returns:
            Optional[str]: The ninth phrase
        """
        return self.parts[8] if len(self.parts) > 8 else None

    @property
    def tenth(self) -> Optional[str]:
        """Tenth phrase

        Returns:
            Optional[str]: The tenth phrase
        """
        return self.parts[9] if len(self.parts) > 9 else None

    def as_list(self) -> list[str]:
        """Convert to a list_doc of strings

        Returns:
            list[str]: The list_doc of strings
        """
        return list(filter(lambda _: _ is not None, self.parts))

    def format(self) -> str:
        """Round tripable format.

        Returns:
            str: The formatted phrases
        """
        # parts = self.as_list()
        usable_parts = []

        def safe_quote(value: str) -> str:
            """Escape spaces and double quotes

            Returns:
                str: The safe quoted string
            """
            if " " in value and '"' not in value:
                return f'"{value}"'
            if " " in value and '"' in value:
                value = value.replace('"', '\\"')
                return f'"{value}'
            return value

        for part in self.parts:
            if part:
                usable_parts.append(part)
            else:
                break

        return " ".join(safe_quote(_) for _ in self.parts if _)

    def validate(self) -> bool:
        """Check if phrases are sensible

        Returns:
            bool: True if phrases are sensible
        """
        return None not in self.parts


@dataclass(frozen=True)
class Command:
    """One parse structure for almost all commands."""

    command: Commands
    line_range: Optional[LineRange] = None
    phrases: Optional[Phrases] = None
    original_text: Optional[str] = dataclasses.field(default=None, compare=False)
    comment: Optional[str] = None

    def validate(self) -> bool:
        """Check if ranges are sensible

        Returns:
            bool: True if ranges are sensible
        """
        if self.line_range:
            line_range_is_valid = self.line_range.validate()
            if not line_range_is_valid:
                return False
        if self.phrases:
            phrases_are_valid = self.phrases.validate()
            if not phrases_are_valid:
                return False
        return True

    def format(self) -> str:
        """Format the command as a string

        Returns:
            str: The formatted command
        """
        if self.command == Commands.COMMENT:
            text = self.comment if self.comment else ""
            return f"# {text}"
        if self.command == Commands.UNKNOWN:
            text = self.original_text if self.original_text else ""
            return f"# Unknown: {text}"
        range_part = self.line_range.format() if self.line_range is not None else ""
        phrase_part = self.phrases.format() if self.phrases is not None else ""
        return " ".join([range_part, self.command.name, phrase_part]).strip()


def try_parse_int(value: str, default_value: Optional[int] = None) -> Optional[int]:
    """Parse int without raising errors

    Args:
        value (str): The value to parse
        default_value (Optional[int]): The default value if parsing fails. Defaults to None.

    Returns:
        Optional[int]: The parsed value
    """
    try:
        return int(value)
    except ValueError:
        if default_value is not None:
            return default_value
        return None


@runtime_checkable
class Printable(Protocol):
    """Something that acts like print()"""

    def __call__(self, text: Optional[str], end: str = "\n") -> None:
        """Signature of a printable.

        Args:
            text (Optional[str]): The text
            end (str): The end. Defaults to "\n".
        """


class NullPrinter:
    """Something that acts like print()"""

    def __call__(self, text: Optional[str], end: str = "\n") -> None:
        """
        Do nothing implementation of Printable.

        Args:
            text (Optional[str]): The text
            end (str): The end. Defaults to "\n".
        """


# def null_printer(text: str, end: str = "") -> None:


@runtime_checkable
class CommandGeneratorProtocol(Protocol):
    """Something stateful and that can generate commands"""

    prompt: str
    document_length: int
    current_line: int

    def generate(
        self,
    ) -> Generator[Command, None, None]:
        """Generate commands.

        Returns:
            Generator[Command, None, None]: The commands
        """


@runtime_checkable
class StringGeneratorProtocol(Protocol):
    """Something stateful and that can generate strings"""

    prompt: str
    default: str

    # current_line:int # will we need this?

    def generate(
        self,
    ) -> Generator[str, None, None]:
        """Generate strings.

        Returns:
            Generator[str, None, None]: The strings
        """

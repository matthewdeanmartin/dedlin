"""
Abstract document class.
"""
import logging
import random
from typing import Callable, Generator, Optional, Tuple

from dedlin.basic_types import LineRange
from dedlin.lorem_data import LOREM_IPSUM
from dedlin.spelling_overlay import check

logger = logging.getLogger(__name__)


# noinspection PyShadowingBuiltins
def print(*args, **kwargs):
    """Discourage accidental usage of print"""
    raise Exception("Don't call UI from here.")


class Document:
    """Abstract document with as few input/output concerns as possible"""

    def __init__(
        self,
        inputter: Callable[[int], Generator[Optional[str], None, None]],
        editor: Callable[[str, str], str],
        lines: list[str],
    ):
        """Set up initial state"""
        self.inputter = inputter
        self.editor = editor
        self.lines: list[str] = lines
        self.current_line: int = 0
        self.previous_lines = lines
        self.previous_current_line = 0
        self.dirty = False

    def list(self, line_range: Optional[LineRange] = None) -> Generator[tuple[str,str], None, None]:
        """Display lines specified by range"""
        if line_range is None or line_range.start == 0 or line_range.end == 0:
            # everything, not an arbitrary cutoff
            line_range = LineRange(1, len(self.lines))

        self.current_line = line_range.start

        # slice handles the case where the range is beyond the end of the document
        for line_text in self.lines[line_range.start - 1 : line_range.end + 1]:
            end = "" if line_text[:-1] == "\n" else "\n"
            yield f"   {self.current_line} : {line_text}", end
            self.current_line += 1

    def search(self, line_range: LineRange, value: str, case_sensitive: bool = False) -> Generator[str, None, None]:
        """Display lines that have value in line"""
        self.current_line = line_range.start

        if not case_sensitive:
            value = value.upper()

        for line_text in self.lines[line_range.start - 1 : line_range.end]:
            if value in line_text.upper():
                yield f"   {self.current_line} : {line_text}"
            self.current_line += 1

    def replace(
        self,
        line_range: Optional[LineRange],
        target: str,
        replacement: str,
        case_sensitive: bool = False,
    ) -> Generator[str, None, None]:
        """Replace target with replacement in lines"""
        # TODO: handle case sensitive case

        if not line_range:
            line_range = LineRange(1, len(self.lines))
        self.current_line = line_range.start - 1

        for line_text in self.lines[line_range.start - 1 : line_range.end]:
            if target in line_text:
                line_text = line_text.replace(target, replacement)
                self.lines[self.current_line] = line_text
                self.dirty = True  # this is ugly
                self.dirty = True  # this is ugly
                yield f"   {self.current_line} : {line_text}"
            self.current_line += 1

    def page(self, page_size: int = 5) -> Generator[tuple[str, str], None, None]:
        """Display lines in pages"""
        line_number = 1
        # TODO: add asterix to new current line
        for line_text in self.lines[self.current_line : self.current_line + page_size]:
            end = "" if line_text[:-1] == "\n" else "\n"
            yield f"   {self.current_line + line_number} : {line_text}", end
            line_number += 1
            if self.current_line >= len(self.lines):
                break
        self.current_line = self.current_line + line_number


    def spell(self, line_range:LineRange) -> Generator[tuple[str, str], None, None]:
        """Show spelling errors in range"""
        line_number = 1
        for line_text in self.lines[line_range.start-1 : line_range.end]:
            end = "" if line_text[:-1] == "\n" else "\n"
            yield f"   {self.current_line + line_number} : {check(line_text)}", end
            line_number += 1
            if self.current_line >= len(self.lines):
                break
        self.current_line = self.current_line + line_number

    def copy(self, line_range: Optional[LineRange], target_line: int) -> None:
        """Copy lines to target_line"""
        if not line_range:
            line_range = LineRange(1, len(self.lines))

        to_copy = self.lines[line_range.start - 1 : line_range.end].copy()
        # doesn't seem efficient but no obvious built-in way to do this
        self.backup()
        self.lines = self.lines[0 : target_line - 1] + to_copy + self.lines[target_line - 1 :]
        self.dirty = True  # this is ugly
        self.current_line = target_line
        logger.debug(f"Copied {line_range} to {target_line}")

    def move(self, line_range: Optional[LineRange], target_line: int):
        """Move lines to target_line"""
        if not line_range:
            raise ValueError("Must specify line range to move")
        if line_range.start < target_line < line_range.end:
            raise ValueError("Cannot move lines within the same range")
        to_copy = self.lines[line_range.start - 1 : line_range.end].copy()

        if not len(to_copy) == line_range.count():
            raise ValueError("Wrong range.")

        self.backup()

        if target_line > line_range.end:
            front = self.lines[0 : target_line + 1]
            back = self.lines[target_line + 1 :]
            self.lines = front + to_copy + back
            deleted = 0
            for index in range(line_range.start - 1, line_range.end):
                self.lines.pop(index - deleted)
                self.dirty = True  # this is ugly
                deleted += 1
        else:
            front = self.lines[0 : target_line - 1]
            back = self.lines[target_line - 1 :]
            self.lines = front + to_copy + back

            deleted = 0
            for index in range(line_range.start + target_line, line_range.end + line_range.count()):
                self.lines.pop(index - deleted)
                self.dirty = True  # this is ugly
                deleted += 1
        self.current_line = target_line
        logger.debug(f"Moving {line_range} to {target_line}")

    def delete(self, line_range: Optional[LineRange]) -> None:
        """Delete lines"""
        if not line_range:
            line_range = LineRange(1, len(self.lines))

        self.list(line_range)

        # TODO: prompt for confirmation

        self.backup()
        for index in range(line_range.end - 1, line_range.start - 2, -1):
            self.lines.pop(index)
            self.dirty = True  # this is ugly
        self.current_line = line_range.start - 1
        logger.debug(f"Deleted {line_range}")

    def fill(self, line_range: LineRange, value: str) -> None:
        """Fill lines with value"""
        self.backup()
        self.current_line = line_range.start
        for index in range(line_range.start, line_range.end):
            self.lines.insert(index, value)
            self.dirty = True  # this is ugly
            self.current_line += 1
        logger.debug(f"Filled {line_range} with {value}")

    def edit(self, line_number: int) -> Optional[int]:
        """Edit line"""
        self.backup()
        line_text = self.lines[line_number - 1]

        try:
            new_line = self.editor(f"   {line_number} : ", line_text[0: len(line_text) - 1])
        except KeyboardInterrupt:
            return None
        self.lines[line_number - 1] = new_line + "\n"
        self.dirty = True  # this is ugly
        self.current_line = line_number
        logger.debug(f"Edited {line_number}")
        if self.current_line > len(self.lines):
            return None
        return self.current_line + 1

    def insert(self, line_number: int) -> None:
        """Insert a new line at line_number"""
        self.backup()
        if line_number < 0:
            line_number = len(self.lines) + 1

        user_input_text: Optional[str] = "GO!"
        input_generator = self.inputter(line_number)
        while user_input_text is not None:
            try:
                user_input_text = next(input_generator)
            except StopIteration:
                user_input_text = None
            if user_input_text is not None:
                self.lines.insert(line_number - 1, user_input_text + "\n")
                self.dirty = True  # this is ugly
                self.current_line = line_number
                line_number += 1
        logger.debug(f"Inserted at {line_number}")

    def lorem(self, line_range: Optional[LineRange]) -> None:
        """Add lorem ipsum to lines"""
        if not line_range:
            line_range = LineRange(1, len(LOREM_IPSUM))

        self.backup()
        # TODO: generate from a specified range of Lorem?
        lines_to_generate = line_range.start
        if lines_to_generate == 0:
            lines_to_generate = len(LOREM_IPSUM)

        for i in range(0, lines_to_generate):
            if i < len(LOREM_IPSUM):
                self.lines.append(LOREM_IPSUM[i])
                self.dirty = True  # this is ugly
        logger.debug(f"Generated {lines_to_generate} lines")

    def undo(self) -> None:
        """Undo last change"""
        self.lines = self.previous_lines
        self.previous_current_line = self.current_line
        logger.debug("Undid last step")

    def sort(self) -> None:
        """Sort lines"""
        self.backup()
        self.lines.sort()
        self.dirty = True  # this is ugly
        logger.debug("Sorted")

    def reverse(self) -> None:
        """Reverse lines"""
        self.backup()
        self.lines = list(reversed(self.lines))
        self.dirty = True  # this is ugly
        logger.debug("Reversed")

    def shuffle(self) -> None:
        """Shuffle lines"""
        self.backup()
        random.shuffle(self.lines)
        self.dirty = True  # this is ugly
        logger.debug("Shuffled")

    def backup(self) -> None:
        """Backup current state"""
        # TODO: call a mutator method instead of assigning to self.previous_lines
        self.previous_lines = self.lines.copy()
        self.previous_current_line = self.current_line

"""
Abstract document class.
"""
import logging
import random
from typing import Callable, Generator, Optional

from dpcontracts import invariant

from dedlin.basic_types import LineRange, Phrases, StringGeneratorProtocol
from dedlin.lorem_data import LOREM_IPSUM
from dedlin.spelling_overlay import check

logger = logging.getLogger(__name__)


# noinspection PyShadowingBuiltins
# pylint: disable=redefined-builtin
def print(*args, **kwargs):
    """Discourage accidental usage of print"""
    raise Exception("Don't call UI from here.")


# What does current line mean when there are 0 lines anyhow? Allow 0 or 1.
# print(self.current_line) is None and
@invariant(
    "Current line must be a valid line",
    lambda self: (1 <= self.current_line <= len(self.lines) or self.current_line in (0, 1) and not self.lines),
)
class Document:
    """Abstract document with as few input/output concerns as possible"""

    def __init__(
        self,
        insert_inputter: StringGeneratorProtocol,
        edit_inputter: Callable[[Optional[str], str], Generator[Optional[str], None, None]],
        lines: list[str],
    ) -> None:
        """Set up initial state"""
        self.insert_inputter = insert_inputter
        self.edit_inputter = edit_inputter
        self.lines: list[str] = lines
        self.current_line: int = 1 if lines else 0
        self.previous_lines = lines
        self.previous_current_line = 0
        self.dirty = False

    def list_doc(self, line_range: Optional[LineRange] = None) -> Generator[tuple[str, str], None, None]:
        """Display lines specified by range"""
        if line_range is None or line_range.start == 0 or line_range.end == 0:
            # everything, not an arbitrary cutoff
            line_range = LineRange(1, len(self.lines) - 1)

        self.current_line = line_range.start

        # slice handles the case where the range is beyond the end of the document
        for line_text in self.lines[line_range.start - 1 : line_range.end + 1]:
            end = "" if line_text[:-1] == "\n" else "\n"
            yield f"   {self.current_line} : {line_text}", end

            # tiny inefficiency here
            if self.current_line >= len(self.lines):
                break
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

    def spread(
        self,
        line_range: Optional[LineRange],
        parts: tuple[str, ...],
    ) -> None:
        """Spread phrases across existing line range"""
        # TODO: handle case sensitive case

        if not line_range:
            line_range = LineRange(1, len(self.lines) - 1)

        end_of_range = len(self.lines) if line_range.end > len(self.lines) else line_range.end
        self.current_line = line_range.start - 1
        for index, line_text in zip(range(line_range.start - 1, end_of_range + 1), parts):
            if line_text:
                self.lines[index] = line_text
                self.dirty = True  # this is ugly
                self.current_line += 1
            else:
                break

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
            line_range = LineRange(1, len(self.lines) - 1)
        self.current_line = line_range.start - 1

        for line_text in self.lines[line_range.start - 1 : line_range.end]:
            if target in line_text:
                line_text = line_text.replace(target, replacement)
                self.lines[self.current_line] = line_text
                self.dirty = True  # this is ugly
                self.dirty = True  # this is ugly
                yield f"   {self.current_line + 1 } : {line_text}"
            self.current_line += 1

    def page(self, page_size: int = 5) -> Generator[tuple[str, str], None, None]:
        """Display lines in pages"""
        line_number = 1
        # TODO: add asterix to new current line
        for line_text in self.lines[self.current_line - 1 : self.current_line + page_size]:
            end = "" if line_text[:-1] == "\n" else "\n"
            yield f"   {self.current_line + line_number} : {line_text}", end
            line_number += 1
            if self.current_line >= len(self.lines):
                break
        if self.current_line + line_number >= len(self.lines):
            self.current_line = len(self.lines)
        else:
            self.current_line = self.current_line + line_number

    def spell(self, line_range: LineRange) -> Generator[tuple[str, str], None, None]:
        """Show spelling errors in range"""
        line_number = 1

        # reset current line to start of range.
        self.current_line = line_range.start
        for line_text in self.lines[line_range.start - 1 : line_range.end]:
            end = "" if line_text[:-1] == "\n" else "\n"
            yield f"   {self.current_line} : {check(line_text)}", end
            self.current_line += 1

    def copy(self, line_range: Optional[LineRange], target_line: int) -> None:
        """Copy lines to target_line"""
        if not line_range:
            line_range = LineRange(1, len(self.lines) - 1)

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
        if not self.lines:
            logger.debug("No lines to delete")
            return
        if not line_range:
            line_range = LineRange(1, len(self.lines) - 1)
        self.list_doc(line_range)

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
        if line_number - 1 < 0:
            raise ValueError("Can't edit negative row.")
        if line_number - 1 >= len(self.lines):
            raise ValueError("Can't edit row that doesn't exist.")

        line_text = self.lines[line_number - 1]

        try:
            new_line = next(self.edit_inputter(f"   {line_number} : ", line_text[0 : len(line_text) - 1]))
        except KeyboardInterrupt:
            return None
        self.lines[line_number - 1] = new_line + "\n"
        self.dirty = True  # this is ugly
        self.current_line = line_number
        logger.debug(f"Edited {line_number}")
        if self.current_line >= len(self.lines):
            return None
        return self.current_line + 1

    def push(self, line_number: int, lines: list[str]) -> None:
        """Noninteractively insert line or lines"""
        self.backup()
        for line in lines:
            self.lines.insert(line_number - 1, line + "\n")
            self.dirty = True  # this is ugly
            self.current_line = line_number
            line_number += 1
            logger.debug(f"Pushed at {line_number}")

    def insert(
        self,
        line_number: int,
        phrases: Optional[Phrases] = None,
    ) -> None:
        """Insert a new line at line_number"""
        self.backup()
        if line_number < 0:
            logger.debug("Autofixing negative line number")
            line_number = 1
        elif line_number > len(self.lines) + 1:
            logger.debug("Autofixing line number beyond end")
            line_number = len(self.lines) + 1

        if phrases:
            for phrase in phrases.as_list():
                self.lines.insert(line_number - 1, phrase + "\n")
                self.dirty = True
                self.current_line = line_number
                line_number += 1
            return

        user_input_text: Optional[str] = "GO!"

        input_generator = self.insert_inputter.generate()
        while user_input_text is not None:
            prompt = f"  {line_number} : "
            self.insert_inputter.prompt = prompt
            try:
                user_input_text = next(input_generator)
            except KeyboardInterrupt:
                user_input_text = None
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
            line_range = LineRange(1, len(LOREM_IPSUM) - 1)

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

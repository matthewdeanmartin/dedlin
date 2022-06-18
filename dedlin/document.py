import logging
from pathlib import Path
import random
from typing import Optional

import questionary

from dedlin.basic_types import LineRange
from dedlin.editable_input_prompt import input_with_prefill
from dedlin.lorem_data import LOREM_IPSUM

logger = logging.getLogger(__name__)


class Document:
    def __init__(self, lines: list[str], file_name: Optional[Path] = None):
        self.lines: list[str] = lines
        self.current_line: int = 0
        self.file_name: Path = file_name
        self.previous_lines = lines
        self.previous_current_line = 0

    def process_list(self, line_range: LineRange):
        self.current_line = line_range.start

        # slice handles the case where the range is beyond the end of the document
        for line_text in self.lines[line_range.start:line_range.end]:
            print(f"   {self.current_line} : {line_text}", end="")
            self.current_line += 1

    def process_search(self, line_range: LineRange, value: str, case_sensitive: bool = False) -> None:
        self.current_line = line_range.start

        if not case_sensitive:
            value = value.upper()

        for line_text in self.lines[line_range.start:line_range.end]:
            if value in line_text.upper():
                print(f"   {self.current_line} : {line_text}", end="")
            self.current_line += 1

    def process_replace(self, line_range: LineRange,
                        target: str,
                        replacement: str) -> None:
        self.current_line = line_range.start

        for line_text in self.lines[line_range.start:line_range.end]:
            if target in line_text:
                line_text = line_text.replace(target, replacement)
                print(f"   {self.current_line} : {line_text}", end="")
            self.current_line += 1

    def process_page(self, page_size: int = 5):
        line_number = 1
        for line_text in self.lines[self.current_line:self.current_line + page_size]:
            end = "" if line_text[:-1] == "\n" else "\n"
            print(f"   {self.current_line + line_number} : {line_text}", end=end)
            line_number += 1
            if self.current_line >= len(self.lines):
                break
        self.current_line = self.current_line + line_number

    def process_copy(self, line_range: LineRange, target_line: int) -> None:
        to_copy = self.lines[line_range.start - 1:line_range.end].copy()
        # doesn't seem efficient but no obvious built-in way to do this
        self.backup()
        self.lines = self.lines[0:target_line - 1] + to_copy + self.lines[target_line - 1:]
        self.current_line = target_line
        logger.debug(f"Copied {line_range} to {target_line}")

    def process_move(self, line_range: LineRange, target_line: int):
        if line_range.start < target_line < line_range.end:
            raise ValueError("Cannot move lines within the same range")
        to_copy = self.lines[line_range.start - 1:line_range.end].copy()

        if not len(to_copy) == line_range.count():
            raise ValueError("Wrong range.")

        self.backup()

        if target_line > line_range.end:
            front = self.lines[0:target_line + 1]
            back = self.lines[target_line + 1:]
            self.lines = front + to_copy + back
            deleted = 0
            for index in range(line_range.start - 1, line_range.end):
                self.lines.pop(index - deleted)
                deleted += 1
        else:
            front = self.lines[0:target_line - 1]
            back = self.lines[target_line - 1:]
            self.lines = front + to_copy + back

            deleted = 0
            for index in range(line_range.start + target_line, line_range.end + line_range.count()):
                self.lines.pop(index - deleted)
                deleted += 1
        self.current_line = target_line
        logger.debug(f"Moving {line_range} to {target_line}")

    def process_delete(self, line_range: LineRange):
        self.backup()
        for index in range(line_range.end - 1, line_range.start - 2, -1):
            self.lines.pop(index)
        self.current_line = line_range.start - 1
        logger.debug(f"Deleted {line_range}")

    def process_fill(self, line_range: LineRange, value: str) -> None:
        self.backup()
        self.current_line = line_range.start
        for index in range(line_range.start, line_range.end):
            self.lines.insert(index, value)
            self.current_line +=1
        logger.debug(f"Filled {line_range} with {value}")

    def process_edit(self, line_number: int) -> None:
        self.backup()
        line_text = self.lines[line_number - 1]
        new_line = input_with_prefill(f"   {line_number} : ", line_text[0:len(line_text) - 1])
        self.lines[line_number - 1] = new_line + "\n"
        self.current_line = line_number
        logger.debug(f"Edited {line_number}")

    def process_insert(self, line_number: int) -> None:
        self.backup()
        if line_number < 0:
            line_number = len(self.lines) + 1

        user_input_text = "GO!"
        while user_input_text:
            user_input_text = questionary.text(f"   {line_number} : ").ask(
                kbi_msg="Exiting insert mode"
            )
            if user_input_text:
                self.lines.insert(line_number - 1, user_input_text + "\n")
                self.current_line = line_number
                line_number += 1
        logger.debug(f"Inserted at {line_number}")

    def process_lorem(self, lines_to_generate: int) -> None:
        self.backup()
        if lines_to_generate == 0:
            lines_to_generate = len(LOREM_IPSUM)

        for i in range(0, lines_to_generate):
            if i < len(LOREM_IPSUM):
                self.lines.append(LOREM_IPSUM[i])
        logger.debug(f"Generated {lines_to_generate} lines")

    def process_undo(self) -> None:
        self.lines = self.previous_lines
        self.previous_current_line = self.current_line
        logger.debug("Undid last step")

    def process_sort(self) -> None:
        self.backup()
        self.lines.sort()
        print("Sorted")
        logger.debug("Sorted")

    def process_reverse(self) -> None:
        self.backup()
        self.lines = [_ for _ in reversed(self.lines)]
        print("Shuffled")
        logger.debug("Shuffled")

    def process_shuffle(self) -> None:
        self.backup()
        random.shuffle(self.lines)
        print("Shuffled")
        logger.debug("Shuffled")

    def backup(self) -> None:
        # TODO: call a mutator method instead of assigning to self.previous_lines
        self.previous_lines = self.lines.copy()
        self.previous_current_line = self.current_line

"""
Main code.
"""
HELP_TEXT = """
Command format: [number],[number] [command] [parameter] [parameter]

Display Commands
[start],[end] List - display lines, set current to end of range
[start],[end] Page - repeat to flipt through entire document
[start],[end] Search [text]

Edit Commands
[line number] Insert - insert line at line number
[line number] Edit - edit number
[start],[end] Delete - delete range
[target] Transfer [file name] - inserts file contents to target
[start],[end] Replace "[text]", "[text]" - replace text in range

Reorder Commands
[start],[end] Move [target line number]
[start],[end] Copy [target line number]
[start],[end] Sort
[start],[end] Shuffle 

File System Commands
Quit
Exit [file name]

"""

import sys
from enum import Enum, auto
from pathlib import Path
from typing import cast, Optional, Any, Tuple, Iterable, Callable, Generator

import questionary
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from dedlin.basic_types import LineRange
from dedlin.document import Document
from dedlin.lorem_data import LOREM_IPSUM


class Commands(Enum):
    Empty = auto()
    List = auto()
    Page = auto()
    Quit = auto()
    Save = auto()
    Insert = auto()
    Edit = auto()
    Delete = auto()
    Help = auto()
    Lorem = auto()
    Undo = auto()
    Unknown = auto()


class Dedlin:
    def __init__(self,
                 inputter: Generator[str, None, None],
                 outputter: Callable[[Optional[str]], None]):
        self.inputter = inputter
        self.outputter = outputter
        self.doc: Optional[Document] = None
        self.halt_on_error = False
        self.echo = False

    def go(self, file_name: Optional[str] = None) -> None:

        if file_name:
            path = Path(file_name)
            print(f"Editing {path.absolute()}")
            lines = read_file(path)
        else:
            path = None
            lines = []

        self.doc = Document(lines=lines, file_name=path)
        while True:
            try:
                user_command_text = next(self.inputter)
            except StopIteration:
                break  # it on down now

            command, params = parse_command(user_command_text,
                                            document_length=len(self.doc.lines))
            self.outputter((command, params))
            if command == Commands.List:
                line_range = cast(LineRange, params)
                self.doc.process_list(line_range)
                self.outputter()
            elif command == Commands.Page:
                # line_range = cast(LineRange, params)
                self.doc.process_page()
                self.outputter()
            elif command == Commands.Delete:
                line_range = cast(LineRange, params)
                self.doc.process_delete(line_range)
                self.outputter(f"Deleted lines {line_range.start} to {line_range.end}")
            elif command == Commands.Save:
                with open(path, "w", encoding="utf-8") as file:
                    file.writelines(self.doc.lines)
                return 0
            elif command == Commands.Quit:
                return 0
            elif command == Commands.Insert:
                line_number = cast(int, params)
                self.doc.process_insert(line_number)
            elif command == Commands.Edit:
                line_number = cast(int, params)
                self.doc.process_edit(line_number)
            elif command == Commands.Lorem:
                line_number = cast(int, params)
                self.doc.process_lorem(line_number)
            elif command == Commands.Undo:
                self.doc.process_undo()
            elif command == Commands.Empty:
                pass
            elif command == Commands.Help:
                self.outputter(HELP_TEXT)
            elif command == Commands.Unknown:
                self.outputter("Unknown command")
                self.outputter(HELP_TEXT)
                if self.halt_on_error:
                    raise Exception(f"Unknown command {user_command_text}")
            else:
                self.outputter("1i to insert at line 1.  E to save and quit. Q to just quit.")
        return 0


def read_file(path):
    lines: list[str] = []

    with open(path, "r") as file:
        for line in file:
            if line.endswith("\n"):
                lines.append(line)
            else:
                lines.append(line + "\n")
    return lines


def extract_one_range(value: str) -> Optional[LineRange]:
    value = value.strip()
    if "," in value:
        parts = value.split(",")
        start = int(parts[0])
        end = int(parts[1])
        return LineRange(start=start, end=end)
    elif value.isnumeric():
        start = int(value)
        return LineRange(start=start, end=start)
    raise TypeError("Could not extract range from value")
    return None


def ends_with_any(value: str, suffixes: Iterable[str]) -> bool:
    if not value:
        return False
    for suffix in suffixes:
        if not suffix:
            continue
        if value.endswith(suffix):
            return True
    return False


def get_command_length(value: str, suffixes: Iterable[str]) -> int:
    for suffix in sorted(suffixes, key=len, reverse=True):
        if value.endswith(suffix):
            return len(suffix)
    return 0


def parse_command(command: str, document_length: int) -> Tuple[Commands, Any]:
    if not command:
        return Commands.Empty, False
    command = command.upper().strip()

    if not command or command.startswith("#"):
        return Commands.Empty, False

    # bare number is insert.
    if command.isnumeric():
        target = int(command)
        # edit end if target is greater than document length.
        return Commands.Edit, target if target <= document_length else document_length

    # TODO: maybe use regex.
    front_part_chars = []
    found_first_alpha = False
    just_command = []
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for char in command:
        if char in alphabet and not found_first_alpha:
            found_first_alpha = True
        if found_first_alpha and char in alphabet:
            just_command.append(char)
        if found_first_alpha and not char in alphabet:
            break
        front_part_chars.append(char)
    # should be numbers
    # ranges
    # ranges with commands
    # but nothing after a command.
    front_part = "".join(front_part_chars)
    end_part = command[len(front_part):]
    if not front_part:
        raise TypeError("Something has gone wrong.")

    # Commands without abbreviations first
    if command in ("UNDO"):
        return Commands.Undo, False

    lorem_commands = ("LOREM",)
    if ends_with_any(front_part, lorem_commands) or front_part in lorem_commands:
        if front_part in lorem_commands:
            return Commands.Lorem, len(LOREM_IPSUM)

        line_count = int(front_part.split("LOREM")[0].strip())
        return Commands.Lorem, line_count

    delete_commands = ("D", "DELETE")
    if ends_with_any(front_part, delete_commands) or front_part in delete_commands:
        if front_part in delete_commands:
            return Commands.Delete, LineRange(start=1, end=document_length)

        command_length = get_command_length(front_part, delete_commands)
        range_text = front_part[0:len(front_part) - command_length]
        line_range = extract_one_range(range_text)
        if line_range:
            return Commands.Delete, line_range

    # Commands with Abbreviations
    list_commands = ("L", "LIST")
    if ends_with_any(front_part, list_commands) or command in list_commands:
        if front_part in list_commands:
            return Commands.List, LineRange(start=0, end=document_length)

        range_text = front_part[0:len(front_part) - 1]
        line_range = extract_one_range(range_text)
        if line_range:
            return Commands.List, line_range

    page_command = ("P", "PAGE")
    if ends_with_any(front_part, page_command) or front_part in page_command:
        # This just increments the pointer
        return Commands.Page, False

    insert_commands = ("I", "INSERT")
    if ends_with_any(front_part, insert_commands) or front_part in insert_commands:
        if front_part in insert_commands:
            return Commands.Insert, -1

        if "INSERT" in front_part:
            line_number = int(front_part.split("INSERT")[0].strip())
            return Commands.Insert, line_number
        else:  # "I" in front_part:
            line_number = int(front_part.split("I")[0].strip())
            return Commands.Insert, line_number

        # line_number = int(command[0:len(command) - 1])
        # return Commands.Insert, line_number

    if command in ("Q", "QUIT"):
        return Commands.Quit, False

    if command in ("E", "EXIT"):
        return Commands.Save, False

    return Commands.Unknown, False


if __name__ == '__main__':
    def run():
        def input_handler(prompt: str = "*") -> Generator[str, None, None]:
            while True:
                answer = questionary.text("*").ask()
                yield answer

        dedlin = Dedlin(input_handler(), print)
        dedlin.go()


    run()

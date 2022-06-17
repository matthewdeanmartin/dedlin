# This is a sample Python script.

import sys
from enum import Enum, auto
from pathlib import Path
from typing import cast, Optional,  Any, Tuple, Iterable

import questionary
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from dedlin.basic_types import LineRange
from dedlin.document import Document

"""
[RANGE] L[ist] 	Displays a range of lines. If no range is specified, L lists the first 23 lines of the file you are editing.
[RANGE] P[age] 	Page. Repeated P with no range specified displays the next 23 lines.

[LINE] I[nsert] 	Inserts new line at the beginning of line specified.
To save the line instead and exit out of the insert menu press <Ctrl> + Z + <Enter>
Press <Ctrl> + <C> to exit out of the insertion.
[LINE] 	Allows the editing of the specified line.
[RANGE] D[elete] 	Deletes a certain range of lines.

[RANGE], [LINE], [NUMBER] C[opy] 	Copies the specified range to the specified line. The number specifies how many copies to do.
[RANGE], [LINE] M[ove] 	Moves a certain range to the specified line.

[RANGE] S[earch] [STRING] 	Searches the current file open for a certain string in quotes!.
[RANGE] R[eplace] [STRING1] [STRING2] 	Searches the specified range for the first specified string if the string is found replaces the string with the second specified string.

[LINE] T [DRIVE:] [\PATH] [FILE] 	Merges the specified file into the current document at the specified line.

Q[uit] 	Quits edlin without saving changes.
E[xit] 	Quits edlin after saving changes.
"""


class Commands(Enum):
    Empty = auto()
    List= auto()
    Page= auto()
    Quit = auto()
    Save = auto()
    Insert = auto()
    Edit = auto()
    Delete = auto()
    Help = auto()

def go(file_name:Optional[str]=None)->None:

    if file_name:
        path = Path(file_name)
        print(f"Editing {path.absolute()}")
        lines = read_file(path)
    else:
        path = None
        lines = []

    doc = Document(lines=lines, file_name=path)
    while True:
        user_command_text = questionary.text("*").ask()
        command, params = parse_command(user_command_text, document_length=len(doc.lines))
        if command == Commands.List:
            line_range = cast(LineRange, params)
            doc.process_list(line_range)
            print()
        elif command == Commands.Page:
            # line_range = cast(LineRange, params)
            doc.process_page()
            print()
        elif command == Commands.Delete:
            line_range = cast( LineRange, params)
            doc.process_delete(line_range)
            print(f"Deleted lines {line_range.start} to {line_range.end}")
        elif command == Commands.Save:
            with open(path, "w", encoding="utf-8") as file:
                file.writelines(doc.lines)
            sys.exit()
        elif command == Commands.Quit:
            sys.exit()
        elif command == Commands.Insert:
            line_number = cast(int, params)
            doc.process_insert(line_number)
        elif command == Commands.Edit:
            line_number = cast(int, params)
            doc.process_edit(line_number)
        elif command == Commands.Empty:
            pass
        else:
            print("1i to insert at line 1.  E to save and quit. Q to just quit.")
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


def extract_one_range(value:str)->Optional[LineRange]:
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

def ends_with_any(value:str, suffixes:Iterable[str])->bool:
    for suffix in suffixes:
        if value.endswith(suffix):
            return True
    return False


def get_command_length(value:str, suffixes:Iterable[str])->int:
    for suffix in sorted(suffixes, key=len, reverse=True):
        if value.endswith(suffix):
            return len(suffix)
    return 0


def parse_command(command:str, document_length:int)->Tuple[Commands, Any]:
    if not command:
        return Commands.Empty, False
    command = command.upper().strip()

    if not command or command.startswith("#"):
        return Commands.Empty, False

    # bare number is insert.
    if command.isnumeric():
        target = int(command)
        # edit end if target is greater than document length.
        return Commands.Edit, target if target<= document_length else document_length

    # TODO: maybe use regex.
    front_part_chars = []
    found_first_alpha = False
    just_command = []
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for char in command:
        if char in alphabet and not found_first_alpha:
            found_first_alpha =True
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

    delete_commands = ("D", "DELETE")
    if ends_with_any(front_part, delete_commands) or front_part in delete_commands:
        if front_part in delete_commands:
            return Commands.Delete, LineRange(start=1, end=document_length)

        command_length = get_command_length(front_part, delete_commands)
        range_text = front_part[0:len(front_part)-command_length]
        line_range = extract_one_range(range_text)
        if line_range:
            return Commands.Delete, line_range

    list_commands = ("L", "LIST")
    if ends_with_any(command, list_commands) or command in list_commands:
        if front_part in list_commands:
            return Commands.List, LineRange(start=0, end=document_length)

        range_text = command[0:len(command)-1]
        line_range = extract_one_range(range_text)
        if line_range:
            return Commands.List, line_range

    page_command = ("P" , "PAGE")
    if ends_with_any(command, page_command) or command in page_command:
        # This just increments the pointer
        return Commands.Page, False

    insert_commands = ("I", "INSERT")
    if ends_with_any(front_part, insert_commands) or front_part in insert_commands:
        if front_part in insert_commands:
            return Commands.Insert, -1

        if "INSERT" in front_part:
            line_number = int(front_part.split("INSERT")[0].strip())
            return Commands.Insert, line_number
        else: # "I" in front_part:
            line_number = int(front_part.split("I")[0].strip())
            return Commands.Insert, line_number

        # line_number = int(command[0:len(command) - 1])
        # return Commands.Insert, line_number

    if command in ("Q", "QUIT"):
        return Commands.Quit, False

    if command in ("E", "EXIT"):
        return Commands.Save, False

    raise TypeError("unknown command")

if __name__ == '__main__':
    go()



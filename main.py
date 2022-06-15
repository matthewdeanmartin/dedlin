# This is a sample Python script.
import sys
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import cast, Optional

import questionary
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from pip._internal.utils.misc import enum

"""
[RANGE] L 	Displays a range of lines. If no range is specified, L lists the first 23 lines of the file you are editing.
[RANGE] P 	Displays listing of range of lines. If no range is specified P displays the complete file. This option is different from L, in that P changes the current line to be the last line.
[RANGE] S [STRING] 	Searches the current file open for a certain string.
[RANGE], [LINE], [NUMBER] C 	Copies the specified range to the specified line. The number specifies how many copies to do.
[RANGE] D 	Deletes a certain range of lines.
[LINE] I 	Inserts new line at the beginning of line specified.
To save the line instead and exit out of the insert menu press <Ctrl> + Z + <Enter>
Press <Ctrl> + <C> to exit out of the insertion.
[RANGE], [LINE] M 	Moves a certain range to the specified line.
[LINE] 	Allows the editing of the specified line.
[RANGE] R [STRING1] [STRING2] 	Searches the specified range for the first specified string if the string is found replaces the string with the second specified string.
[NUMBER] A 	Reads the number of lines into memory.
[LINE] T [DRIVE:] [\PATH] [FILE] 	Merges the specified file into the current document at the specified line.
[NUMBER] W 	Writes the specified number of lines onto disk.
Q 	Quits edlin without saving changes.
E 	Quits edlin after saving changes.
"""

import readline

def input_with_prefill(prompt, text):
    # ref https://stackoverflow.com/a/8505387
    def hook():
        readline.insert_text(text)
        readline.redisplay()
    readline.set_pre_input_hook(hook)
    result = input(prompt)
    readline.set_pre_input_hook()
    return result

class Commands(Enum):
    Empty = auto()
    List= auto()
    Print= auto()
    Quit = auto()
    Save = auto()
    Insert = auto()
    Edit = auto()
    Delete = auto()


def go(file_name:str):
    path = Path(file_name)
    print(f"Editing {path.absolute()}")
    current_line = 0
    lines:list[str] = []
    with open(path, "r") as file:
        for line in file:
            if line.endswith("\n"):
                lines.append(line)
            else:
                lines.append(line + "\n")
    while True:
        user_command_text = questionary.text("*").ask()
        command, params = parse_command(user_command_text)
        if command == Commands.List:
            line_number = 1
            line_range = cast( LineRange, params)
            for line_text in lines[line_range.start:line_range.end]:
                print(f"   {line_number} : {line_text}", end="")
                line_number += 1
            print()
        if command == Commands.Delete:
            line_range = cast( LineRange, params)
            for index in range(line_range.end-1, line_range.start-2, -1):
                lines.pop(index)
            print(f"Deleted lines {line_range.start} to {line_range.end}")
        elif command == Commands.Save:
            with open(path, "w", encoding="utf-8") as file:
                file.writelines(lines)
            sys.exit()
        elif command == Commands.Quit:
            sys.exit()
        elif command == Commands.Insert:
            line = cast(int, params)
            user_input_text = "GO!"
            while user_input_text:
                user_input_text = questionary.text(f"   {line} : ").ask(
                    kbi_msg="Exiting insert mode"
                )
                if user_input_text:
                    lines.insert(line-1, user_input_text + "\n")
                    line +=1
        elif command == Commands.Edit:
            # this is not cross-platform
            # TODO: https://stackoverflow.com/a/11616477
            line_number = cast(int, params)
            line_text = lines[line_number-1]
            new_line = input_with_prefill(f"   {line_number} : ", line_text[0:len(line_text)-1])
            lines[line_number-1] = new_line + "\n"
        else:
            print("1i to insert at line 1.  E to save and quit. Q to just quit.")

@dataclass
class LineRange():
    start:int
    end:int

def extract_one_range(value:str)->Optional[LineRange]:
    if "," in value:
        parts = value.split(",")
        start = int(parts[0])
        end = int(parts[1])
        return LineRange(start=start, end=end)
    elif value.isnumeric():
        start = int(value)
        return LineRange(start=start, end=start)
    return None

def parse_command(command:str):
    if not command:
        return Commands.Empty, False
    command = command.upper().strip()
    if command.isnumeric():
        return Commands.Edit, int(command)
    if command.endswith("D"):
        range_text = command[0:len(command)-1]
        line_range = extract_one_range(range_text)
        if line_range:
            return Commands.Delete, line_range
    if command.endswith("L") or command == "L":
        if command == "L":
            return Commands.List, LineRange(start=0, end=23-1)

        range_text = command[0:len(command)-1]
        line_range = extract_one_range(range_text)
        if line_range:
            return Commands.List, line_range
    if command.endswith("I"):
        line = int(command[0:len(command) - 1])
        return Commands.Insert, line
    if command == "Q":
        return Commands.Quit, False
    if command == "E":
        return Commands.Save, False

    raise TypeError("unknown command")

if __name__ == '__main__':
    go("file.txt")

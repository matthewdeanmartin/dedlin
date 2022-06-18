"""
Code that turns strings to command objects
"""

from typing import Iterable, Optional, Tuple

from dedlin.basic_types import Command, Commands, LineRange, Phrases
from dedlin.lorem_data import LOREM_IPSUM


def extract_one_range(value: str) -> Optional[LineRange]:
    """Extract a single line range from a string"""
    value = value.strip()
    if "," in value:
        parts = value.split(",")
        start = int(parts[0])
        end = int(parts[1]) if len(parts) > 1 else start
        repeat = int(parts[2]) if len(parts) > 2 else 1
        return LineRange(start=start, end=end, repeat=repeat)
    if value.isnumeric():
        start = int(value)
        return LineRange(start=start, end=start, repeat=1)
    return None


def extract_phrases(value: str) -> Optional[Phrases]:
    """Extract phrases from a string"""
    # handle quotes without escapes
    if '"' in value and '\\"' not in value:
        parts = [_ for _ in value.split('"') if _.strip() != ""]
        if len(parts) == 1:
            return Phrases(parts[0], "")
        if len(parts) > 1:
            return Phrases(parts[0], parts[1])

    # handle unquoted delimited by spaces
    if '"' not in value:
        parts = [_ for _ in value.split(" ") if _.strip() != ""]
        if len(parts) == 1:
            return Phrases(parts[0].strip(), "")
        if len(parts) > 1:
            return Phrases(parts[0].strip(), parts[1].strip())

    if '\\"' in value:
        raise NotImplementedError("Escape quotes not implemented")

    return None


def ends_with_any(value: str, suffixes: Iterable[str]) -> bool:
    """Apply endswith to lines of text"""
    if not value:
        return False
    for suffix in suffixes:
        if not suffix:
            continue
        if value.endswith(suffix):
            return True
    return False


def get_command_length(value: str, suffixes: Iterable[str]) -> int:
    """Get the length of the command"""
    for suffix in sorted(suffixes, key=len, reverse=True):
        if value.endswith(suffix):
            return len(suffix)
    return 0


def parse_simple_command(command: str, original_text: str) -> Optional[Command]:
    """Parse a command that has no line range or phrases"""
    # Commands without abbreviations first
    if command in ("UNDO",):
        return Command(
            Commands.Undo,
            original_text=original_text,
        )

    if command in ("SHUFFLE",):
        return Command(
            Commands.Shuffle,
            original_text=original_text,
        )
    if command in ("SORT",):
        return Command(
            Commands.Sort,
            original_text=original_text,
        )
    if command in ("REVERSE",):
        return Command(
            Commands.Reverse,
            original_text=original_text,
        )
    return None


def parse_search_replace(
    command_forms: Tuple[str, str],
    command_code: Commands,
    front_part: str,
    phrases: Optional[Phrases],
    original_text: str,
) -> Optional[Command]:
    """Parse a command that has a line range and phrases"""
    if ends_with_any(front_part, command_forms) or front_part in command_forms:
        abbreviation, long_command = command_forms
        if front_part in command_forms:
            line_range = None
        elif long_command in front_part:
            line_number = int(front_part.split(long_command)[0].strip())
            line_range = LineRange(start=line_number, end=line_number)
        else:
            line_number = int(front_part.split(abbreviation)[0].strip())
            line_range = LineRange(start=line_number, end=line_number)
        return Command(
            command_code,
            line_range=line_range,
            phrases=phrases,
            original_text=original_text,
        )
    return None


def parse_command(command: str, document_length: int) -> Command:
    """Parse a command"""
    original_text = command
    original_text_upper = command.upper()
    if not command:
        return Command(
            command=Commands.Empty,
            original_text=original_text,
        )

    command = command.upper().strip()

    if not command or command.startswith("#"):
        return Command(
            command=Commands.Empty,
            original_text=original_text,
        )

        # bare number is insert.
    if command.isnumeric():
        target = int(command)
        # edit end if target is greater than document length.
        target = target if target <= document_length else document_length
        return Command(
            command=Commands.Edit,
            line_range=LineRange(start=target, end=target),
            original_text=original_text,
        )

    # TODO: maybe use regex.
    front_part_chars = []
    found_first_alpha = False
    just_command_chars = []
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for char in command:
        if char in alphabet and not found_first_alpha:
            found_first_alpha = True
        if found_first_alpha and char in alphabet:
            just_command_chars.append(char)
        if found_first_alpha and not char in alphabet:
            break
        front_part_chars.append(char)

    front_part = "".join(front_part_chars)
    just_command = "".join(just_command_chars)
    location_of_command = original_text_upper.find(just_command)

    end_part = original_text[location_of_command + len(just_command) :]
    if end_part:
        # must preserve case!
        phrases = extract_phrases(end_part)
    else:
        phrases = None

    if not front_part:
        raise TypeError("Something has gone wrong.")

    candidate = parse_simple_command(front_part, original_text)
    if candidate:
        return candidate

    lorem_commands = ("LOREM",)
    if ends_with_any(front_part, lorem_commands) or front_part in lorem_commands:
        if front_part in lorem_commands:
            line_count = len(LOREM_IPSUM)
            line_range = LineRange(start=1, end=line_count, repeat=1)
        else:
            line_count = int(front_part.split("LOREM")[0].strip())
            line_range = LineRange(start=1, end=line_count, repeat=1)
        return Command(
            Commands.Lorem,
            line_range=line_range,
            original_text=original_text,
        )

    delete_commands = ("D", "DELETE")
    if ends_with_any(front_part, delete_commands) or front_part in delete_commands:
        if front_part in delete_commands:
            line_range: Optional[LineRange] = LineRange(start=1, end=document_length)
        else:
            command_length = get_command_length(front_part, delete_commands)
            range_text = front_part[0 : len(front_part) - command_length]
            line_range = extract_one_range(range_text)

        return Command(
            Commands.Delete, line_range=line_range, original_text=original_text
        )

    # Commands with Abbreviations
    list_commands = ("L", "LIST")
    if ends_with_any(front_part, list_commands) or command in list_commands:
        if front_part in list_commands:
            line_range = LineRange(start=0, end=document_length)
        else:
            range_text = front_part[0 : len(front_part) - 1]
            line_range = extract_one_range(range_text)
        return Command(
            Commands.List, line_range=line_range, original_text=original_text
        )

    page_command = ("P", "PAGE")
    if ends_with_any(front_part, page_command) or front_part in page_command:
        if front_part in list_commands:
            line_range = LineRange(start=0, end=document_length)
        else:
            range_text = front_part[0 : len(front_part) - 1]
            line_range = extract_one_range(range_text)
        return Command(
            Commands.Page, line_range=line_range, original_text=original_text
        )

    insert_commands = ("I", "INSERT")
    if ends_with_any(front_part, insert_commands) or front_part in insert_commands:
        if front_part in insert_commands:
            line_range = None
        elif "INSERT" in front_part:
            line_number = int(front_part.split("INSERT")[0].strip())
            line_range = LineRange(start=line_number, end=line_number)
        else:  # "I" in front_part:
            line_number = int(front_part.split("I")[0].strip())
            line_range = LineRange(start=line_number, end=line_number)
        return Command(
            Commands.Insert, line_range=line_range, original_text=original_text
        )

    command_forms = ("S", "SEARCH")
    candidate = parse_search_replace(
        command_forms, Commands.Search, front_part, phrases, original_text
    )
    if candidate:
        return candidate

    command_forms = ("R", "REPLACE")
    candidate = parse_search_replace(
        command_forms, Commands.Replace, front_part, phrases, original_text
    )
    if candidate:
        return candidate

    if command in ("Q", "QUIT"):
        return Command(Commands.Quit, original_text=original_text)

    if command in ("E", "EXIT"):
        return Command(Commands.Exit, original_text=original_text)

    return Command(Commands.Unknown, original_text=original_text)

"""
Code that turns strings to command objects
"""

from typing import Iterable, Optional

from dedlin.basic_types import Command, Commands, LineRange, Phrases, try_parse_int


def extract_one_range(value: str, current_line: int, document_length: int) -> Optional[LineRange]:
    """Extract a single line range from a string
    . = current line
    $ = last line
    """
    value = value.strip()
    if "," in value:
        parts = value.split(",")
        start_string = parts[0]
        if start_string == ".":
            start = current_line
        elif start_string == "$":
            start = document_length
        else:
            start = try_parse_int(start_string)
        end_string = parts[1]
        if end_string == ".":
            end = current_line
        elif end_string == "$":
            end = document_length
        else:
            end = try_parse_int(parts[1]) if len(parts) > 1 else start

        repeat = try_parse_int(parts[2]) if len(parts) > 2 else 1

        if start == 1 and end == 0:
            end = 1 if document_length == 0 else document_length

        # TODO: need better parser errors
        if start is None or end is None or repeat is None:
            print("Range invalid:", value)
            return None

        candidate = LineRange(start=start, end=end, repeat=repeat)

        # TODO: need better parser errors
        if not candidate.validate():
            print("Candidate invalid:", candidate)
            return None

        return candidate
    if value == ".":
        return LineRange(start=current_line, end=current_line, repeat=1)
    if value == "$":
        return LineRange(start=document_length, end=document_length, repeat=1)
    if value and all(_ in "0123456789" for _ in value):
        start = int(value)
        candidate = LineRange(start=start, end=start, repeat=1)

        # TODO: need better parser errors
        if not candidate.validate():
            print("Candidate invalid:", candidate)
            return None
        return candidate
    return None


def extract_phrases(value: str) -> Optional[Phrases]:
    """Extract phrases from a string"""
    # handle quotes without escapes
    if '"' in value and '\\"' not in value:
        parts = [_ for _ in value.split('"') if _.strip() != ""]

        kwarg_names = ["first", "second", "third", "fourth", "fifth"]
        kwargs = {}
        for part, name in zip(parts, kwarg_names):
            if part:
                kwargs[name] = part
        if kwargs:
            return Phrases(**kwargs)

    # handle unquoted delimited by spaces
    if '"' not in value:
        parts = [_ for _ in value.split(" ") if _.strip() != ""]
        if len(parts) == 1:
            return Phrases(parts[0].strip(), None)
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


RANGE_ONLY = {
    Commands.LOREM: ("LOREM",),
    Commands.DELETE: ("D", "DELETE"),
    Commands.EDIT: ("EDIT",),
    Commands.INSERT: ("I", "INSERT"),
    Commands.LIST: ("L", "LIST"),
    Commands.PAGE: ("P", "PAGE"),
    Commands.SPELL: ("SPELL",),
    Commands.SEARCH: ("S", "SEARCH"),  # 1 phrase
    Commands.REPLACE: ("R", "REPLACE"),  # 2 phrases
    Commands.EXIT: ("X", "EXIT"),
    Commands.TRANSFER: ("T", "TRANSFER"),
    Commands.HISTORY: ("HISTORY",),
    Commands.MACRO: ("MACRO",),
    Commands.BROWSE: ("BROWSE",),
    Commands.CURRENT: ("CURRENT",),
    Commands.SHUFFLE: ("SHUFFLE",),
    Commands.SORT: ("SORT",),
    Commands.REVERSE: ("REVERSE",),
}


def parse_range_only(
    just_command: str,
    front_part: str,
    original_text: str,
    current_line: int,
    document_length: int,
    phrases: Optional[Phrases],
) -> Optional[Command]:
    """Parse a command that has a line range"""
    # TODO: the biggest generic parser should replace all of these
    for command_code, command_forms in RANGE_ONLY.items():
        if just_command in command_forms:
            if front_part in command_forms:
                line_range: Optional[LineRange] = LineRange(start=1, end=1 if document_length == 0 else document_length)
            else:
                command_length = get_command_length(front_part, command_forms)
                range_text = front_part[0 : len(front_part) - command_length]
                line_range = extract_one_range(range_text, current_line, document_length)

            return Command(
                command_code,
                line_range=line_range,
                phrases=phrases,
                original_text=original_text,
            )
    return None


COMMANDS_WITH_PHRASES = {
    Commands.SEARCH: ("S", "SEARCH"),  # 1 phrase
    Commands.REPLACE: ("R", "REPLACE"),  # 2 phrases
    Commands.HELP: ("HELP",),
    Commands.PUSH: ("PUSH",),
}


def parse_search_replace(
    front_part: str,
    phrases: Optional[Phrases],
    original_text: str,
) -> Optional[Command]:
    """Parse a command that has a line range and phrases"""
    for command_code, command_forms in COMMANDS_WITH_PHRASES.items():
        if ends_with_any(front_part, command_forms) or front_part in command_forms:
            if len(command_forms) == 2:
                abbreviation, long_command = command_forms
            else:
                abbreviation, long_command = None, command_forms[0]

            line_range = None
            if front_part in command_forms:
                line_range = None
            elif long_command in front_part:
                line_number_string = front_part.split(long_command)[0].strip()
                line_number = try_parse_int(line_number_string)
                if line_number is None:
                    print("Bad range", original_text)
                    return None
                line_range = LineRange(start=line_number, end=line_number)
            elif abbreviation is not None:
                line_number = try_parse_int(front_part.split(abbreviation)[0].strip())
                if line_number is None:
                    print("Bad range", original_text)
                    return None

                line_range = LineRange(start=line_number, end=line_number)

            return Command(
                command_code,
                line_range=line_range,
                phrases=phrases,
                original_text=original_text,
            )
    return None


BARE_COMMANDS = {
    Commands.HISTORY: ("H", "HISTORY"),
    Commands.REDO: ("REDO",),
    Commands.UNDO: ("UNDO",),
    Commands.EXIT: ("E", "EXIT"),  # BUG, this takes argument.
    Commands.QUIT: ("Q", "QUIT"),
}


def bare_command(command: str) -> Optional[Command]:
    """Parse a command that has no line range or phrases"""
    for command_code, command_forms in BARE_COMMANDS.items():
        if command in command_forms:
            return Command(
                command_code,
                original_text=command,
            )
    return None


def parse_command(command: str, current_line: int, document_length: int) -> Command:
    """Parse a command"""
    original_text = command
    if not command:
        return Command(
            command=Commands.EMPTY,
            original_text=original_text,
        )

    original_text_upper = command.upper()
    command = command.upper().strip()

    if not command or command.startswith("#"):
        return Command(
            command=Commands.EMPTY,
            original_text=original_text,
        )

        # bare number is insert.
    candidate_int = try_parse_int(command)
    if candidate_int is not None:
        target = candidate_int
        # edit end if target is greater than document length.
        target = target if target <= document_length else document_length
        return Command(
            command=Commands.EDIT,
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

    # Meaning of range shifted, need to fix.
    # lorem_commands = ("LOREM",)
    # if ends_with_any(front_part, lorem_commands) or front_part in lorem_commands:
    #     if front_part in lorem_commands:
    #         line_count = len(LOREM_IPSUM)
    #         line_range = LineRange(start=1, end=line_count, repeat=1)
    #     else:
    #         line_count = try_parse_int(front_part.split("LOREM", maxsplit=1)[0].strip())
    #         line_range = LineRange(start=1, end=line_count, repeat=1)
    #     return Command(
    #         Commands.LOREM,
    #         line_range=line_range,
    #         original_text=original_text,
    #     )

    candidate = parse_range_only(just_command, front_part, original_text, current_line, document_length, phrases)
    if candidate:
        return candidate

    candidate = parse_search_replace(front_part, phrases, original_text)
    if candidate:
        return candidate

    # This where range is 1 row.. monoparse it! ignore teh range end
    # insert_commands = ("I", "INSERT")
    # if ends_with_any(front_part, insert_commands) or front_part in insert_commands:
    #     if front_part in insert_commands:
    #         line_range = None
    #     elif "INSERT" in front_part:
    #         line_number = try_parse_int(front_part.split("INSERT", maxsplit=1)[0].strip())
    #         if line_number is None:
    #             print("Invalid target", command)
    #             return None
    #         line_range = LineRange(start=line_number, end=line_number)
    #     else:  # "I" in front_part:
    #         line_number = try_parse_int(front_part.split("I", maxsplit=1)[0].strip())
    #         if line_number is None:
    #             print("Invalid target", command)
    #             return None
    #         line_range = LineRange(start=line_number, end=line_number)
    #     return Command(Commands.INSERT, line_range=line_range, original_text=original_text)

    candidate = bare_command(command)
    if candidate:
        return candidate

    return Command(Commands.UNKNOWN, original_text=original_text)


if __name__ == "__main__":
    result = parse_command("1i cat dog", 1, 0)
    result = parse_command("1", 1, 3)
    print(result)
    print(result.validate())

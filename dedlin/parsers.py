"""
Code that turns strings to command objects
"""
import logging
from typing import Iterable, Optional

from dedlin.basic_types import Command, Commands, LineRange, Phrases, try_parse_int

logger = logging.getLogger(__name__)


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
            logger.warning(f"Range invalid:{value}. start:{start}, end:{end}, repeat:{repeat}")
            return None

        candidate = LineRange(start=start, offset=end - start, repeat=repeat)

        # TODO: need better parser errors
        if not candidate.validate():
            logger.warning(f"Candidate invalid: {candidate}")
            return None

        return candidate
    if value == ".":
        return LineRange(start=current_line, offset=0, repeat=1)
    if value == "$":
        return LineRange(start=document_length, offset=0, repeat=1)
    if value and all(_ in "0123456789" for _ in value):
        start = int(value)
        if start <= 1:
            start = 1
        candidate = LineRange(start=start, offset=0, repeat=1)

        # TODO: need better parser errors
        if not candidate.validate():
            logger.warning(f"Candidate invalid: {candidate}")
            return None
        return candidate
    return None


def extract_phrases(value: str) -> Optional[Phrases]:
    """Extract phrases from a string"""
    # handle quotes without escapes
    if '"' in value and '\\"' not in value:
        parts = [_ for _ in value.split('"') if _.strip() != ""]
        return Phrases(tuple(parts))

    # handle unquoted delimited by spaces
    if '"' not in value:
        parts = [_ for _ in value.split(" ") if _.strip() != ""]
        return Phrases(parts=parts)
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
    # String Commands
    Commands.TITLE: ("TITLE",),
    Commands.SWAPCASE: ("SWAPCASE",),
    Commands.CASEFOLD: ("CASEFOLD",),
    Commands.CAPITALIZE: ("CAPITALIZE",),
    Commands.UPPER: ("UPPER",),
    Commands.LOWER: ("LOWER",),
    Commands.EXPANDTABS: ("EXPANDTABS",),
    Commands.RJUST: ("RJUST",),
    Commands.LJUST: ("LJUST",),
    Commands.CENTER: ("CENTER",),
    Commands.RSTRIP: ("RSTRIP",),
    Commands.LSTRIP: ("LSTRIP",),
    Commands.STRIP: ("STRIP",),
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
                line_range: Optional[LineRange] = LineRange(
                    start=1, offset=0 if document_length == 0 else document_length - 1
                )
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
    Commands.COPY: ("COPY",),  # 1 phrase
    Commands.MOVE: ("MOVE",),  # 1 phrase
    Commands.SEARCH: ("S", "SEARCH"),  # 1 phrase
    Commands.REPLACE: ("R", "REPLACE"),  # 2 phrases
    Commands.HELP: ("HELP",),
    Commands.PUSH: ("PUSH",),
    Commands.CRASH: ("CRASH",),
    Commands.EXPORT: ("EXPORT",),
}


def parse_search_replace(
    front_part: str, phrases: Optional[Phrases], original_text: str, current_line: int, document_length: int
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
                # line_number_string = front_part.split(long_command)[0].strip()
                # line_number = try_parse_int(line_number_string)
                # line_range = LineRange(start=line_number, offset=0)
                line_range = extract_one_range(front_part.replace(long_command, ""), current_line, document_length)
                if line_range is None:
                    logger.warning(f"Bad range {original_text}")
                    return None
            elif abbreviation is not None:
                # line_number = try_parse_int(front_part.split(abbreviation)[0].strip())
                # line_range = LineRange(start=line_number, offset=0)
                line_range = extract_one_range(front_part.replace(long_command, ""), current_line, document_length)
                if line_range is None:
                    logger.warning(f"Bad range {original_text}")
                    return None
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

    # Handle empty text.
    if not command:
        return Command(
            command=Commands.EMPTY,
            original_text=original_text,
        )

    original_text_upper = command.upper()
    command = command.upper().strip()

    # Handle comments
    if not command or command.startswith("#"):
        return Command(
            command=Commands.EMPTY,
            original_text=original_text,
        )

    # Handle shortcuts, bare number is insert.
    candidate_int = try_parse_int(command)
    if candidate_int is not None:
        target = candidate_int
        # edit end if target is greater than document length.
        target = target if target <= document_length else document_length
        if document_length == 0:
            print("Can't edit empty document. Use INSERT")
            return Command(Commands.UNKNOWN, original_text=original_text)
        if document_length < target:
            print("Can't edit beyond end of document.")
            return Command(Commands.UNKNOWN, original_text=original_text)
        return Command(
            command=Commands.EDIT,
            line_range=LineRange(start=target, offset=0),
            original_text=original_text,
        )

    # Divide into
    # - front part (pre command)
    # - command
    # - phrases (post command)
    front_part_chars = []
    found_first_alpha = False
    just_command_chars = []
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for char in command:
        if char in alphabet and not found_first_alpha:
            found_first_alpha = True
        if found_first_alpha and char in alphabet:
            just_command_chars.append(char)
        if found_first_alpha and char not in alphabet:
            break
        front_part_chars.append(char)

    front_part = "".join(front_part_chars)
    just_command = "".join(just_command_chars)
    location_of_command = original_text_upper.find(just_command)

    # Handle post command phrases
    end_part = original_text[location_of_command + len(just_command) :]
    if end_part:
        # must preserve case!
        phrases = extract_phrases(end_part)
    else:
        phrases = None

    if not front_part:
        raise TypeError("Something has gone wrong.")

    candidate = parse_range_only(just_command, front_part, original_text, current_line, document_length, phrases)
    if candidate:
        return candidate

    candidate = parse_search_replace(front_part, phrases, original_text, current_line, document_length)
    if candidate:
        return candidate

    candidate = bare_command(command)
    if candidate:
        return candidate

    return Command(Commands.UNKNOWN, original_text=original_text)

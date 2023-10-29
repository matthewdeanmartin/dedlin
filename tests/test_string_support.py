from dedlin.basic_types import Command, Commands, Phrases
from dedlin.parsers import extract_phrases
from dedlin.string_comands import block_commands, process_strings


def test_block_commands():
    lines = ["a", "b"]
    command = Command(Commands.INDENT, phrases=Phrases(parts=("    ",)))
    assert block_commands(lines, command) == ["    a", "    b"]
    lines = ["    a", "    b"]
    command = Command(Commands.DEDENT)
    assert block_commands(lines, command) == ["a", "b"]


def test_process_strings():
    for kind in [
        # String commands
        Commands.TITLE,
        Commands.SWAPCASE,
        Commands.CASEFOLD,
        Commands.CAPITALIZE,
        Commands.UPPER,
        Commands.LOWER,
        Commands.EXPANDTABS,
        Commands.RJUST,
        Commands.LJUST,
        Commands.CENTER,
        Commands.RSTRIP,
        Commands.LSTRIP,
        Commands.STRIP,
    ]:
        command = Command(kind, phrases=extract_phrases("1"))
        # just make sure it doesn't crash
        lines = ["a"]
        process_strings(lines, command)
        assert lines[0]

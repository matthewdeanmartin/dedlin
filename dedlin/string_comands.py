import textwrap

from dedlin.basic_types import Commands, Command

COMMANDS_WITH_PHRASES = {
    # String Commands
    Commands.TRIM
}


def block_commands(lines: list[str], command: Command):
    """String manipulation for whole range as a unit, not line per line"""

    # doesn't need to use preferred line break
    block = "\n".join(lines)
    if command.command == Commands.INDENT:
        block = textwrap.indent(block, command.phrases.first)
    if command.command == Commands.DEDENT:
        block = textwrap.dedent(block)
    return "\n".split(block)


def process_strings(lines: list[str], command: Command):
    """Apply string function to each line"""
    for index, line in enumerate(lines):
        # leading and trailing space

        if command.command == Commands.STRIP:
            lines[index] = line.strip()
        elif command.command == Commands.LSTRIP:
            lines[index] = line.lstrip()
        elif command.command == Commands.RSTRIP:
            lines[index] = line.rstrip()
        elif command.command == Commands.CENTER:
            lines[index] = line.center(int(command.phrases.first))
        elif command.command == Commands.LJUST:
            lines[index] = line.ljust(int(command.phrases.first))
        elif command.command == Commands.RJUST:
            lines[index] = line.rjust(int(command.phrases.first))
        elif command.command == Commands.EXPANDTABS:
            lines[index] = line.expandtabs(int(command.phrases.first))
        # capitalization
        elif command.command == Commands.LOWER:
            lines[index] = line.lower()
        elif command.command == Commands.UPPER:
            lines[index] = line.upper()
        elif command.command == Commands.CAPITALIZE:
            lines[index] = line.capitalize()
        elif command.command == Commands.CASEFOLD:
            lines[index] = line.casefold()
        elif command.command == Commands.SWAPCASE:
            lines[index] = line.swapcase()
        elif command.command == Commands.TITLE:
            lines[index] = line.title()
        else:
            raise NotImplementedError()

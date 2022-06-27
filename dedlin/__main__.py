"""Dedlin.

An improved version of the edlin.

Usage:
  dedlin <file> [options]
  dedlin (-h | --help)
  dedlin --version

Options:
  -h --help          Show this screen.
  --version          Show version.
  --macro=<macro>    Run macro file.
  --echo             Echo commands.
  --halt_on_error    End program on error.
  --promptless_quit  Skip prompt on quit.
  --vim_mode         User hostile, no feedback.
"""
import sys
from pathlib import Path
from typing import Optional

from docopt import docopt

from dedlin.command_sources import interactive_command_handler, command_generator
from dedlin.editable_input_prompt import input_with_prefill
from dedlin.flash import title_screen
from dedlin.main import Dedlin
from dedlin.rich_output import RichPrinter


def main()->None:
    """Main function."""
    arguments = docopt(__doc__, version="1.4.0")
    _ = run(
        arguments["<file>"],
        echo=bool(arguments["--echo"]),
        halt_on_error=bool(arguments["--halt_on_error"]),
        macro_file_name=arguments["--macro"],
        quit_safety=not arguments["--promptless_quit"],
        vim_mode=bool(arguments["--vim_mode"]),
    )
    sys.exit(0)


def run(
        file_name: Optional[str] = None,
        macro_file_name: Optional[str] = None,
        echo: bool = False,
        halt_on_error: bool = False,
        quit_safety: bool = False,
        vim_mode: bool = False,
) -> Dedlin:
    """Set up everything except things from command line"""
    if not macro_file_name:
        title_screen()

    rich_printer = RichPrinter()

    def printer(text, end="\n"):
        rich_printer.print(text, end="")

    if macro_file_name:
        command_handler = command_generator(Path(macro_file_name))
    else:
        command_handler = interactive_command_handler()
    dedlin = Dedlin(command_handler,
                    input_with_prefill,
                    printer if file_name and file_name.endswith(".py") else print)
    dedlin.halt_on_error = halt_on_error
    dedlin.echo = echo
    dedlin.quit_safety = quit_safety
    dedlin.vim_mode = vim_mode
    dedlin.entry_point(file_name, macro_file_name)
    return dedlin


if __name__ == "__main__":
    main()

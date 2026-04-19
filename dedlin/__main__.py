"""Dedlin.

An improved version of the edlin.
"""

import argparse
import logging
import logging.config
import sys
import traceback
from pathlib import Path

from dedlin.__about__ import __version__
from dedlin.command_sources import (
    CommandGenerator,
    InteractiveGenerator,
    StringCommandGenerator,
)
from dedlin.document_sources import PrefillInputter, SimpleInputter
from dedlin.flash import title_screen
from dedlin.logging_utils import configure_logging
from dedlin.main import Dedlin
from dedlin.outputters import rich_output, talking_outputter
from dedlin.outputters.plain import plain_printer
from dedlin.ui_exit import confirm_exit

logger = logging.getLogger(__name__)


def main() -> None:
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Dedlin. An improved version of the edlin.", formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("--version", action="version", version=__version__)

    # Global options
    parser.add_argument("-e", "--echo", action="store_true", help="Echo commands.")
    parser.add_argument("--halt-on-error", action="store_true", help="End program on error.")
    parser.add_argument("--promptless-quit", action="store_true", help="Skip prompt on quit.")
    parser.add_argument("--vim-mode", action="store_true", help="User hostile, no feedback.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Displaying all debugging info.")
    parser.add_argument("--blind-mode", action="store_true", help="Optimize for blind users (experimental).")
    parser.add_argument("--headless", action="store_true", help="Run without interactive prompts.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Prevent actual file modification and print a unified diff to stdout instead.",
    )
    parser.add_argument(
        "--diff", action="store_true", help="Print a unified diff of the changes made at the end of the session."
    )

    subparsers = parser.add_subparsers(dest="subcommand", help="Subcommands")

    # Edit subcommand
    parser_edit = subparsers.add_parser("edit", help="Start an interactive session")
    parser_edit.add_argument("file", nargs="?", help="File to edit")

    # Exec subcommand
    parser_exec = subparsers.add_parser("exec", help="Run inline commands")
    parser_exec.add_argument("file", help="File to edit")
    parser_exec.add_argument("-c", "--command", action="append", required=True, help="Command to run")

    # Macro subcommand
    parser_macro = subparsers.add_parser("macro", help="Run a macro file")
    parser_macro.add_argument("macro_file", help="Macro file to run")
    parser_macro.add_argument("file", help="File to edit")

    # Stream subcommand
    parser_stream = subparsers.add_parser("stream", help="Read from stdin, process, write to stdout")
    parser_stream.add_argument("-c", "--command", action="append", required=True, help="Command to run")

    args, unknown = parser.parse_known_args()

    # Fallback to edit if no subcommand but there's a file
    if args.subcommand is None:
        if unknown:
            args.file = unknown[0]
            args.subcommand = "edit"
        else:
            args.subcommand = "edit"
            args.file = None

    _ = run(args)
    sys.exit(0)


def run(args: argparse.Namespace) -> Dedlin:
    """Set up everything except things from command line.

    Args:
        args: The argparse parsed arguments.

    Returns:
        Dedlin: The dedlin object.
    """
    if args.verbose:
        config = configure_logging()
        logging.config.dictConfig(config)
        logger.info("Verbose mode enabled")

    # Determine command generator and headless mode
    macro_file_name = None
    headless = args.headless
    initial_lines = None
    file_name = None

    if args.subcommand == "edit":
        file_name = args.file
        the_command_generator = InteractiveGenerator()
        the_command_generator.prompt = " * "
    elif args.subcommand == "macro":
        macro_file_name = args.macro_file
        file_name = args.file
        the_command_generator = CommandGenerator(Path(macro_file_name))
        headless = True
    elif args.subcommand == "exec":
        file_name = args.file
        commands_str = "\\n".join(args.command)
        the_command_generator = StringCommandGenerator(commands_str)
        headless = True
    elif args.subcommand == "stream":
        commands_str = "\\n".join(args.command)
        the_command_generator = StringCommandGenerator(commands_str)
        initial_lines = sys.stdin.read().splitlines()
        headless = True
    else:
        the_command_generator = InteractiveGenerator()
        the_command_generator.prompt = " * "

    if not macro_file_name and not headless:
        title_screen(args.blind_mode)

    if args.blind_mode:
        logger.info("Blind mode. UI should talk.")
        printer = talking_outputter.printer
        args.echo = True
    elif file_name and file_name.endswith(".py"):
        logger.info("Rich mode. UI should be colorful.")
        printer = rich_output.printer
    else:
        logger.info("Plain mode. UI should be dull.")
        printer = plain_printer

    dedlin = Dedlin(
        inputter=the_command_generator,
        insert_document_inputter=SimpleInputter(),
        edit_document_inputter=PrefillInputter(),
        outputter=printer,
        headless=headless,
        dry_run=args.dry_run,
        diff=args.diff,
        stream_output=(args.subcommand == "stream"),
    )

    dedlin.halt_on_error = args.halt_on_error
    dedlin.echo = args.echo
    dedlin.quit_safety = not args.promptless_quit
    dedlin.vim_mode = args.vim_mode
    dedlin.verbose = args.verbose

    while True:
        # pylint: disable=broad-except
        try:
            sys.excepthook = dedlin.save_on_crash
            dedlin.entry_point(file_name, macro_file_name, initial_lines=initial_lines)
            if not args.vim_mode:
                break
        except KeyboardInterrupt:
            confirm_exit(-1, None)
            if not args.vim_mode:
                break

        except Exception as the_exception:
            dedlin.save_on_crash(type(the_exception), the_exception, None)
            print(traceback.format_exc())
            break

    dedlin.final_report()
    return dedlin


if __name__ == "__main__":
    main()

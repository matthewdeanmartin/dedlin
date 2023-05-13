"""Dedlin.

An improved version of the edlin.

Usage:
  dedlin [<file>] [options]
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
  --verbose          Displaying all debugging info.
  --blind_mode       Optimize for blind users (experimental).
"""
import logging
import logging.config
import sys
import traceback
from pathlib import Path
from typing import Generator, Optional

from docopt import docopt

from dedlin.command_sources import CommandGenerator, InteractiveGenerator
from dedlin.document_sources import PrefillInputter, SimpleInputter, input_with_prefill
from dedlin.flash import title_screen
from dedlin.logging_utils import configure_logging
from dedlin.main import Dedlin
from dedlin.outputters import rich_output, talking_outputter
from dedlin.outputters.plain import plain_printer

logger = logging.getLogger(__name__)


def main() -> None:
    """Main function."""
    arguments = docopt(__doc__, version="1.4.0")
    _ = run(
        arguments["<file>"],
        echo=bool(arguments["--echo"]),
        halt_on_error=bool(arguments["--halt_on_error"]),
        macro_file_name=arguments["--macro"],
        quit_safety=not arguments["--promptless_quit"],
        vim_mode=bool(arguments["--vim_mode"]),
        verbose=bool(arguments["--verbose"]),
        blind_mode=bool(arguments["--blind_mode"]),
    )
    sys.exit(0)


def run(
    file_name: Optional[str] = None,
    macro_file_name: Optional[str] = None,
    echo: bool = False,
    halt_on_error: bool = False,
    quit_safety: bool = False,
    vim_mode: bool = False,
    verbose: bool = False,
    blind_mode: bool = False,
) -> Dedlin:
    """Set up everything except things from command line"""
    if verbose:
        config = configure_logging()
        logging.config.dictConfig(config)
        logger.info("Verbose mode enabled")

    if not macro_file_name:
        title_screen(blind_mode)

    if blind_mode:
        logger.info("Blind mode. UI should talk.")
        printer = talking_outputter.printer
        echo = True
    elif file_name and file_name.endswith(".py"):
        logger.info("Rich mode. UI should be colorful.")
        printer = rich_output.printer
    else:
        logger.info("Plain mode. UI should be dull.")
        printer = plain_printer

    if macro_file_name:
        the_command_generator = CommandGenerator(Path(macro_file_name))
        # command_handler = the_generator.generate()
    else:
        the_command_generator = InteractiveGenerator()
        the_command_generator.prompt = " * "
        # command_handler = the_interactive_generator.generate()

    def document_inputter(prompt: str, text: str = "") -> Generator[str, None, None]:
        """Get input from the user"""
        while True:
            yield input_with_prefill(prompt, text)

    dedlin = Dedlin(
        inputter=the_command_generator,  # InteractiveGenerator(),
        insert_document_inputter=SimpleInputter(),
        edit_document_inputter=PrefillInputter(),
        outputter=printer,
    )

    # save on crash but hides error info
    # sys.excepthook = lambda type, value, tb: dedlin.save_document() if dedlin.doc.dirty else None

    dedlin.halt_on_error = halt_on_error
    dedlin.echo = echo
    dedlin.quit_safety = quit_safety
    dedlin.vim_mode = vim_mode
    dedlin.verbose = verbose
    while True:
        # pylint: disable=broad-except
        try:
            sys.excepthook = dedlin.save_on_crash
            dedlin.entry_point(file_name, macro_file_name)
            if not vim_mode:
                break
        except KeyboardInterrupt:
            if not vim_mode:
                break
        except Exception as the_exception:
            dedlin.save_on_crash(the_exception, None, None)
            print(traceback.format_exc())
            break
    dedlin.final_report()
    return dedlin


if __name__ == "__main__":
    main()

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

from docopt import docopt

from dedlin.main import run


def main():
    """Main function."""
    arguments = docopt(__doc__, version="0.1.0")
    # print(arguments)
    result = run(
            arguments["<file>"],
            echo=True if arguments["--echo"] else False,
            halt_on_error=True if arguments["--halt_on_error"] else False,
            macro_file_name=arguments["--macro"],
            quit_safety=not arguments["--promptless_quit"],
            vim_mode=True if arguments["--vim_mode"] else False,
        )
    sys.exit(0)


if __name__ == "__main__":
    main()

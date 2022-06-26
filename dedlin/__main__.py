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


if __name__ == "__main__":
    main()

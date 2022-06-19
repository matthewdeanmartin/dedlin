"""
Command line entrypoint
"""
import sys

from dedlin.main import run


def entry_point():
    """Entrypoint for python -m dedlin"""
    args = sys.argv[1:]
    file = args[0] if args else ""

    sys.exit(run(file))


if __name__ == "__main__":
    entry_point()

"""
Command line entrypoint
"""
import sys

from dedlin.main import run


def go():
    """Entrypoint for python -m dedlin"""
    args = sys.argv[1:]
    if args:
        file = args[0]
    sys.exit(run(str(file)))


if __name__ == "__main__":
    go()

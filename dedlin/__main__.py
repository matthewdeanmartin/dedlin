"""
Command line entrypoint
"""
import sys

from dedlin.main import run


def go():
    """Entrypoint for python -m dedlin"""
    file = sys.argv[1:]
    sys.exit(run(str(file)))


if __name__ == "__main__":
    go()

import logging.config
from pathlib import Path

from dedlin.basic_types import command_generator
from dedlin.logging_utils import configure_logging
from dedlin.main import Dedlin


def test_lorem_ed():
    LOGGING_CONFIG = configure_logging()

    logging.config.dictConfig(LOGGING_CONFIG)

    lines_path = Path("sample_files/animals.txt")
    macro_path = Path("sample_macros/lorem.ed")

    dedlin = Dedlin(command_generator(macro_path), print)
    dedlin.halt_on_error = True
    dedlin.quit_safety = False
    dedlin.go(str(lines_path.absolute()))
    assert dedlin.doc.lines


def test_shuffle_sort_reverse_ed():
    LOGGING_CONFIG = configure_logging()

    logging.config.dictConfig(LOGGING_CONFIG)

    lines_path = Path("sample_files/animals.txt")
    macro_path = Path("sample_macros/randomize.ed")

    dedlin = Dedlin(command_generator(macro_path), print)
    dedlin.halt_on_error = True
    dedlin.quit_safety = False
    dedlin.go(str(lines_path.absolute()))
    assert dedlin.doc.lines


def test_degenerate_ed():
    LOGGING_CONFIG = configure_logging()

    logging.config.dictConfig(LOGGING_CONFIG)

    macro_path = Path("sample_macros/degenerate.ed")

    dedlin = Dedlin(command_generator(macro_path), print)
    dedlin.halt_on_error = False
    dedlin.go()
    assert not dedlin.doc.lines


def test_search_ed():
    LOGGING_CONFIG = configure_logging()

    logging.config.dictConfig(LOGGING_CONFIG)

    lines_path = Path("sample_files/animals.txt")
    macro_path = Path("sample_macros/grep.ed")
    thing = []

    def capture(line, end="\n"):
        thing.append(line)

    dedlin = Dedlin(command_generator(macro_path), capture)
    dedlin.halt_on_error = True
    dedlin.go(str(lines_path.absolute()))
    for line in thing:
        assert "cat" in line


def test_replace_ed():
    LOGGING_CONFIG = configure_logging()

    logging.config.dictConfig(LOGGING_CONFIG)

    lines_path = Path("sample_files/animals.txt")
    macro_path = Path("sample_macros/sed.ed")
    thing = []

    def capture(line, end="\n"):
        thing.append(line)

    dedlin = Dedlin(command_generator(macro_path), capture)
    dedlin.halt_on_error = True
    dedlin.quit_safety = False
    dedlin.go(str(lines_path.absolute()))
    for line in dedlin.doc.lines:
        assert "giraffe" not in line
    assert "butt\n" in dedlin.doc.lines

import logging.config
from pathlib import Path

from dedlin.basic_types import command_generator
from dedlin.logging_utils import configure_logging
from dedlin.main import Dedlin
from dedlin.utils.file_utils import locate_file

ANIMALS_FILE = Path(locate_file("sample_files/animals.txt", __file__))


def test_lorem_ed():
    LOGGING_CONFIG = configure_logging()

    logging.config.dictConfig(LOGGING_CONFIG)

    lines_path = ANIMALS_FILE
    macro_path = Path(locate_file("sample_macros/lorem.ed", __file__))

    dedlin = Dedlin(command_generator(macro_path), print)
    dedlin.halt_on_error = True
    dedlin.quit_safety = False
    dedlin.entry_point(str(lines_path.absolute()))
    assert dedlin.doc.lines


def test_shuffle_sort_reverse_ed():
    LOGGING_CONFIG = configure_logging()

    logging.config.dictConfig(LOGGING_CONFIG)

    lines_path = ANIMALS_FILE
    macro_path = Path(locate_file("sample_macros/randomize.ed", __file__))

    dedlin = Dedlin(command_generator(macro_path), print)
    dedlin.halt_on_error = True
    dedlin.quit_safety = False
    dedlin.entry_point(str(lines_path.absolute()))
    assert dedlin.doc.lines


def test_degenerate_ed():
    LOGGING_CONFIG = configure_logging()

    logging.config.dictConfig(LOGGING_CONFIG)

    macro_path = Path(locate_file("sample_macros/degenerate.ed", __file__))

    dedlin = Dedlin(command_generator(macro_path), print)
    dedlin.halt_on_error = False
    dedlin.entry_point()
    assert not dedlin.doc.lines


def test_search_ed():
    LOGGING_CONFIG = configure_logging()

    logging.config.dictConfig(LOGGING_CONFIG)

    lines_path = ANIMALS_FILE
    macro_path = Path(locate_file("sample_macros/grep.ed", __file__))
    thing = []

    def capture(line, end="\n"):
        thing.append(line)

    dedlin = Dedlin(command_generator(macro_path), capture)
    dedlin.halt_on_error = True
    dedlin.entry_point(str(lines_path.absolute()))
    for line in thing:
        assert "cat" in line


def test_replace_ed():
    LOGGING_CONFIG = configure_logging()

    logging.config.dictConfig(LOGGING_CONFIG)

    lines_path = ANIMALS_FILE
    macro_path = Path(locate_file("sample_macros/sed.ed", __file__))
    thing = []

    def capture(line, end="\n"):
        thing.append(line)

    dedlin = Dedlin(command_generator(macro_path), capture)
    dedlin.halt_on_error = True
    dedlin.quit_safety = False
    dedlin.entry_point(str(lines_path.absolute()))
    for line in dedlin.doc.lines:
        assert "giraffe" not in line
    assert "butt\n" in dedlin.doc.lines

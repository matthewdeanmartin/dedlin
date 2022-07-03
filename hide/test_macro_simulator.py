"""
Simulates user entry from a macro file using generate
"""
import logging.config
from pathlib import Path
from typing import Generator

from dedlin.basic_types import Command
from dedlin.command_sources import CommandGenerator
from dedlin.logging_utils import configure_logging
from dedlin.main import Dedlin
from dedlin.utils.file_utils import locate_file

ANIMALS_FILE = Path(locate_file("sample_files/animals.txt", __file__))


def document_inputter_that_blows_up(line: str, end: str) -> Generator[Command, None, None]:
    raise TypeError("This script is supposed to take no input")


def test_lorem_ed():
    LOGGING_CONFIG = configure_logging()

    logging.config.dictConfig(LOGGING_CONFIG)

    lines_path = ANIMALS_FILE
    macro_path = Path(locate_file("sample_macros/lorem.ed", __file__))
    string_generator = CommandGenerator()
    dedlin = Dedlin(string_generator.generate(macro_path), document_inputter_that_blows_up, print)
    dedlin.halt_on_error = True
    dedlin.quit_safety = False
    dedlin.entry_point(str(lines_path.absolute()))
    assert dedlin.doc.lines


def test_shuffle_sort_reverse_ed():
    LOGGING_CONFIG = configure_logging()

    logging.config.dictConfig(LOGGING_CONFIG)

    lines_path = ANIMALS_FILE
    macro_path = Path(locate_file("sample_macros/randomize.ed", __file__))
    string_generator = CommandGenerator()
    dedlin = Dedlin(string_generator.generate(macro_path), document_inputter_that_blows_up, print)
    dedlin.halt_on_error = True
    dedlin.quit_safety = False
    dedlin.entry_point(str(lines_path.absolute()))
    assert dedlin.doc.lines


def test_degenerate_ed():
    LOGGING_CONFIG = configure_logging()

    logging.config.dictConfig(LOGGING_CONFIG)

    macro_path = Path(locate_file("sample_macros/degenerate.ed", __file__))
    string_generator = CommandGenerator()
    dedlin = Dedlin(string_generator.generate(macro_path), document_inputter_that_blows_up, print)
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

    string_generator = CommandGenerator()
    dedlin = Dedlin(string_generator.generate(macro_path), document_inputter_that_blows_up, capture)
    dedlin.halt_on_error = True
    dedlin.quiet = True
    dedlin.entry_point(str(lines_path.absolute()))
    for line in thing:
        assert "cat" in line


# def test_replace_ed():
#     LOGGING_CONFIG = configure_logging()
#
#     logging.config.dictConfig(LOGGING_CONFIG)
#
#     lines_path = ANIMALS_FILE
#     macro_path = Path(locate_file("sample_macros/sed.ed", __file__))
#     thing = []
#
#     def capture(line, end="\n"):
#         thing.append(line)
#
#     string_generator = CommandGenerator()
#     dedlin = Dedlin(string_generator.generate(macro_path),
#                     document_inputter_that_blows_up, capture)
#     dedlin.halt_on_error = True
#     dedlin.quit_safety = False
#     dedlin.entry_point(str(lines_path.absolute()))
#     # already gone by this point
#     # assert "giraffe\n" in dedlin.doc.lines
#     found = False
#     for line in dedlin.doc.lines:
#         assert "giraffe\n" not in line
#         found = True
#     assert found
#     assert "butt\n" in dedlin.doc.lines

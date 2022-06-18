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
    dedlin.go(str(lines_path.absolute()))
    assert dedlin.doc.lines

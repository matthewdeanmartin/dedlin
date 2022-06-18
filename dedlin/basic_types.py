import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Generator

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class LineRange:
    start:int
    end:int

    def count(self):
        return self.end - self.start + 1

    def validate(self):
        validate= 1 <= self.start <= self.end and self.end >= 1
        if not validate:
            logger.warning(f"Invalid line range: {self}")
        return validate


def command_generator(macro_path: Path) -> Generator[str, None, None]:
    with open(str(macro_path), "r") as file:
        for line in file:
            yield line
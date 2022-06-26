"""
Class for reading and writing lines to disk.

This could be document lines or macro lines.
"""
from pathlib import Path
from typing import Optional


def read_or_create_file(path: Path) -> list[str]:
    """Attempt to read file, create if it doesn't exist"""
    if path:
        print(f"Editing {path.absolute()}")
        if not path.exists():
            with open(str(path.absolute()), "w", encoding="utf-8") as file:
                pass
        lines = read_file(path)
    else:
        lines = []
    return lines


def read_file(path: Optional[Path]) -> list[str]:
    """Read a file and return a list_doc of lines"""
    lines: list[str] = []

    with open(path, encoding="utf-8") as file:
        for line in file:
            if line.endswith("\n"):
                lines.append(line)
            else:
                lines.append(line + "\n")
    return lines


def save_and_overwrite(path: Path, lines: list[str]):
    """Save a file and overwrite it"""
    if not path:
        raise TypeError("No file path")
    with open(str(path), "w", encoding="utf-8") as file:
        file.seek(0)
        file.writelines(lines)

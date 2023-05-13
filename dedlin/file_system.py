"""
Class for reading and writing lines to disk.

This could be document lines or macro lines.
"""
from pathlib import Path
from typing import Optional

from dedlin.tools.export import export_markdown


def read_or_create_file(path: Path) -> list[str]:
    """Attempt to read file, create if it doesn't exist"""

    if path:
        print(f"Editing {path.absolute()}")
        if not path.exists():
            with open(str(path.absolute()), "w", encoding="utf-8"):
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
                lines.append(line[:-1])
            elif line.endswith("\r"):
                lines.append(line[:-1])
            elif line.endswith("\r\n") or line.endswith("\n\r"):
                lines.append(line[:-2])
            else:
                lines.append(line)
    return lines


def save_and_overwrite(path: Path, lines: list[str], preferred_line_break: str) -> None:
    """Save a file and overwrite it"""
    if not path:
        raise TypeError("No file path")
    with open(str(path), "w", encoding="utf-8") as file:
        file.seek(0)
        file.writelines(line + preferred_line_break for line in lines)


def export(path: Path, lines: list[str], preferred_line_break: str) -> None:
    """Save a file and overwrite it"""
    if not path:
        raise TypeError("No file path")
    if path.suffix.lower() == ".html":
        html_name = path.rename(path.with_suffix(".html"))
        with open(str(html_name), "w", encoding="utf-8") as file:
            file.seek(0)
            file.write(export_markdown(lines, preferred_line_break))
    else:
        with open(str(path), "w", encoding="utf-8") as file:
            file.seek(0)
            # TODO: make this use preferred line break
            file.writelines(line + "\n" for line in lines)

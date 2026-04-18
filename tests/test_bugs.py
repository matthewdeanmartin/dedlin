from pathlib import Path

import dedlin.file_system as file_system
from dedlin.basic_types import Command, Commands, LineRange, Phrases
from dedlin.command_sources import InMemoryCommandGenerator
from dedlin.document import Document
from dedlin.document_sources import InMemoryInputter
from dedlin.main import Dedlin
from tests.fakes import fake_edit, fake_input


def test_lorem_bug_repro():
    """LOREM command should be able to generate more than 20 lines."""
    doc = Document(fake_input, fake_edit, [])
    # 1,50 LOREM should generate 50 lines
    doc.lorem(LineRange(start=1, offset=49))
    assert len(doc.lines) == 50


def test_search_bug_repro():
    """SEARCH command should display correct line numbers."""
    doc = Document(fake_input, fake_edit, ["apple", "banana", "cherry", "apple pie"])
    results = list(doc.search(LineRange(1, 3), "apple"))
    # results are strings like "   1 : apple"
    # apple pie is at index 4, but we search range 1-4 (LineRange(1,3) is 1,2,3,4)
    # Wait, LineRange(1, 3) is start=1, offset=3, so end=4.
    line_numbers = [r.strip().split(":")[0].strip() for r in results]
    assert line_numbers == ["1", "4"]


def test_move_command_bug_repro():
    """Dedlin.entry_point should call doc.move for MOVE command."""
    # Move line 1 to position 3 (after line 2)
    # LineRange(1, 0) is just line 1.
    commands = [
        Command(Commands.MOVE, line_range=LineRange(1, 0), phrases=Phrases(("3",))),
        Command(Commands.EXIT),
    ]
    lines = ["line 1", "line 2", "line 3"]

    # We need to write lines to a file first because entry_point reads from it
    p = Path("test_move_repro.txt")
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")

    try:
        app = Dedlin(
            inputter=InMemoryCommandGenerator(commands),
            insert_document_inputter=InMemoryInputter([]),
            edit_document_inputter=InMemoryInputter([]),
            outputter=lambda x, y="": None,
        )
        app.entry_point(file_name=str(p))
        # Moving line 1 to position 3: ["line 2", "line 1", "line 3"]
        assert app.doc.lines == ["line 2", "line 1", "line 3"]
    finally:
        if p.exists():
            p.unlink()


def test_read_file_crlf_bug_repro():
    """read_file should correctly handle CRLF."""
    p = Path("test_crlf_repro.txt")
    with open(p, "wb") as f:
        f.write(b"line1\r\nline2\r\n")
    try:
        lines = file_system.read_file(p)
        assert lines == ["line1", "line2"]
    finally:
        if p.exists():
            p.unlink()


def test_save_without_filename_crash_repro():
    """Dedlin should not crash when saving without a filename in headless mode."""
    commands = [
        Command(Commands.SAVE),
        Command(Commands.EXIT),
    ]
    # Headless mode requires a filename at entry_point if none in constructor,
    # but the bug was that SAVE would try to use self.file_path which might be None.
    # Actually, entry_point(file_name=None) in headless mode raises TypeError.
    # So the "save without filename" crash is when we ARE in headless but forgot to provide it?
    # No, the user said "Launch with dedlin, no file name, and try to save and it blows up."

    app = Dedlin(
        inputter=InMemoryCommandGenerator(commands),
        insert_document_inputter=InMemoryInputter([]),
        edit_document_inputter=InMemoryInputter([]),
        outputter=lambda x, y="": None,
        headless=False,  # Let's test non-headless first to see if it prompts or crashes
    )

    # Mocking input() to avoid hang
    import builtins

    original_input = builtins.input
    builtins.input = lambda _: ""  # Return empty string for filename
    try:
        app.entry_point()
    finally:
        builtins.input = original_input
    # Should not crash

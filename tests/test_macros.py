"""
Headless scripts do not need a companion file.
"""

from pathlib import Path

import pytest

from dedlin import CommandGenerator, Dedlin, StringCommandGenerator
from dedlin.utils.exceptions import DedlinException
from dedlin.utils.file_utils import locate_file


def test_macros():
    for file in [
        "grep.ed",
        "sed.ed",
        "walrus_facts1.ed",
        "walrus_facts2.ed",
        "walrus_facts3.ed",
    ]:
        degenerate = Path(locate_file(f"sample_macros/{file}", __file__))
        commandGenerator = CommandGenerator(degenerate)
        results = []
        # pylint: disable=cell-var-from-loop
        app = Dedlin(
            inputter=commandGenerator,
            insert_document_inputter=None,
            edit_document_inputter=None,
            outputter=lambda x, end: results.append(x),
            headless=True,
        )

        # Read in the input file so we can copy it.
        with open(
            locate_file(f"sample_macros/{file.replace('.ed','_in.txt')}", __file__), encoding="utf-8"
        ) as input_file:
            pristine_input = input_file.read()
        output_file = f"sample_macros/{file.replace('.ed','_out.txt')}"

        # Write to a file that can be mutated
        with open(locate_file(output_file, __file__), "w", encoding="utf-8") as pristine_file:
            pristine_file.write(pristine_input)

        app.entry_point(file_name=locate_file(output_file, __file__))

        # Log results
        output_file = f"sample_macros/{file.replace('.ed', '_log.txt')}"
        with open(locate_file(output_file, __file__), "w", encoding="utf-8") as log_file:
            for line in results:
                log_file.write(line)
                log_file.write("\n")

        # TODO: add snapshot testing logic.


def _run_headless_session(file_path: Path, command_source: str) -> Dedlin:
    results = []
    app = Dedlin(
        inputter=StringCommandGenerator(command_source),
        insert_document_inputter=None,
        edit_document_inputter=None,
        outputter=lambda x, end: results.append(x),
        headless=True,
    )
    _ = app.entry_point(file_name=str(file_path))
    return app


def test_in_session_macro_runs_against_current_document(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    document = tmp_path / "notes.txt"
    document.write_text("alpha\n", encoding="utf-8")
    macro = tmp_path / "cleanup.ed"
    macro.write_text("1 REPLACE alpha beta\n", encoding="utf-8")

    app = _run_headless_session(document, "MACRO cleanup.ed")

    assert app.doc is not None
    assert app.doc.lines == ["beta"]


def test_nested_macro_resolves_relative_paths(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    document = tmp_path / "notes.txt"
    document.write_text("alpha\n", encoding="utf-8")
    macro_dir = tmp_path / "macros"
    macro_dir.mkdir()
    parent_macro = macro_dir / "parent.ed"
    child_macro = macro_dir / "child.ed"
    parent_macro.write_text("MACRO child.ed\n", encoding="utf-8")
    child_macro.write_text("1 REPLACE alpha beta\n", encoding="utf-8")

    app = _run_headless_session(document, "MACRO macros/parent.ed")

    assert app.doc is not None
    assert app.doc.lines == ["beta"]


def test_macro_recursion_is_rejected(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    document = tmp_path / "notes.txt"
    document.write_text("alpha\n", encoding="utf-8")
    macro_a = tmp_path / "a.ed"
    macro_b = tmp_path / "b.ed"
    macro_c = tmp_path / "c.ed"
    macro_a.write_text("MACRO b.ed\n", encoding="utf-8")
    macro_b.write_text("MACRO c.ed\n", encoding="utf-8")
    macro_c.write_text("MACRO a.ed\n", encoding="utf-8")

    with pytest.raises(DedlinException, match="Macro recursion detected"):
        _run_headless_session(document, "MACRO a.ed")


def test_macro_nesting_stops_after_level_three(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    document = tmp_path / "notes.txt"
    document.write_text("alpha\n", encoding="utf-8")
    macro_a = tmp_path / "a.ed"
    macro_b = tmp_path / "b.ed"
    macro_c = tmp_path / "c.ed"
    macro_d = tmp_path / "d.ed"
    macro_a.write_text("MACRO b.ed\n", encoding="utf-8")
    macro_b.write_text("MACRO c.ed\n", encoding="utf-8")
    macro_c.write_text("MACRO d.ed\n", encoding="utf-8")
    macro_d.write_text("1 REPLACE alpha beta\n", encoding="utf-8")

    with pytest.raises(DedlinException, match=r"Macro nesting limit reached \(3\)"):
        _run_headless_session(document, "MACRO a.ed")


@pytest.mark.parametrize("quit_command", ["QUIT", "EXIT"])
def test_macro_quit_and_exit_stop_the_full_app(tmp_path: Path, monkeypatch, quit_command: str):
    monkeypatch.chdir(tmp_path)
    document = tmp_path / "notes.txt"
    document.write_text("alpha\n", encoding="utf-8")
    macro = tmp_path / "stop.ed"
    macro.write_text(f"1 REPLACE alpha beta\n{quit_command}\n1 REPLACE beta gamma\n", encoding="utf-8")

    app = _run_headless_session(document, "MACRO stop.ed\n1 REPLACE beta omega")

    assert app.doc is not None
    assert app.doc.lines == ["beta"]

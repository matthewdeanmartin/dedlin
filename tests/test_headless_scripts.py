"""
Headless scripts do not need a companion file.
"""

from pathlib import Path

from dedlin import CommandGenerator, Dedlin
from dedlin.utils.file_utils import locate_file


def test_headless(tmp_path: Path):
    for file in [
        "degenerate.ed",
        "lorem.ed",
        "news.ed",
        "randomize.ed",
        "robo.ed",
        "walrus_facts.ed",
        "walrus_facts2.ed",
    ]:
        degenerate = Path(locate_file(f"sample_headless_scripts/{file}", __file__))
        commandGenerator = CommandGenerator(degenerate)
        results = []
        # pylint: disable=cell-var-from-loop
        app = Dedlin(
            inputter=commandGenerator,
            insert_document_inputter=None,
            edit_document_inputter=None,
            outputter=lambda text, end="", start_line=0: results.append(text),
            headless=True,
        )
        snapshot_file = tmp_path / f"{file}_snapshot.txt"
        app.entry_point(str(snapshot_file))
        assert results

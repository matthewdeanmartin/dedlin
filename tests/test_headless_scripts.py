"""
Headless scripts do not need a companion file.
"""
from pathlib import Path

from dedlin import CommandGenerator, Dedlin
from dedlin.utils.file_utils import locate_file


def test_headless():
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
        app = Dedlin(
            inputter=commandGenerator,
            insert_document_inputter=None,
            edit_document_inputter=None,
            outputter=lambda x, _: results.append(x),
            headless=True,
        )
        app.entry_point(locate_file(f"sample_headless_scripts/{file}_snapshot.txt", __file__))
        assert results

from dedlin.basic_types import LineRange
from dedlin.document import Document
from tests.fakes import fake_edit, fake_input


def test_list():
    lines = ["1", "2", "3", "4"]
    doc = Document(fake_input, fake_edit, lines)
    current = doc.current_line
    assert current == 1

    result = list(doc.list_doc(LineRange(1, offset=0)))
    assert len(result) == 1
    assert ": 1" in result[0][0]
    assert doc.current_line == current

    result = list(doc.list_doc(LineRange(2, offset=1)))
    assert len(result) == 2
    assert ": 2" in result[0][0]
    assert ": 3" in result[1][0]
    assert doc.current_line == current

    result = list(doc.list_doc(LineRange(1, offset=20)))
    assert len(result) == 4
    for i in lines:
        assert f": {i}" in result[int(i) - 1][0]
    assert doc.current_line == current


def test_page():
    lines = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
    doc = Document(fake_input, fake_edit, lines)
    assert doc.current_line == 1
    current = doc.current_line

    result = list(doc.page(5))
    assert len(result) == 5
    assert ": 1" in result[0][0]
    assert doc.current_line == 6
    assert doc.current_line != current

    result = list(doc.page(5))
    assert len(result) == 5
    assert ": 6" in result[0][0]
    assert doc.current_line == 11
    assert doc.current_line != current

    result = list(doc.page(5))
    assert len(result) == 2
    assert ": 11" in result[0][0]
    assert doc.current_line == 12
    assert doc.current_line != current


def test_spell():
    # no obvious errors
    lines = ["I can't spell", "But I can write", "Line by line, I will keep on writing"]
    doc = Document(fake_input, fake_edit, lines)
    results = list(doc.spell(LineRange(1, 1000)))
    for result in results:
        assert "did you mean" not in result[0]
    assert len(results) == 3

    # with errors
    lines = ["I can't spoll", "But I can wraete", "Line by line, I vaill keep on writing"]
    doc = Document(fake_input, fake_edit, lines)
    results = list(doc.spell(LineRange(1, 1000)))
    for result in results:
        assert "did you mean" in result[0]
    assert len(results) == 3


def test_search():
    # no obvious errors
    lines = ["cat dog rabbit rot", "bird dinosaur raptor rot", "cabbage carrot celery"]
    doc = Document(fake_input, fake_edit, lines)
    results = list(doc.search(LineRange(1, 1000), "cat", case_sensitive=False))
    for result in results:
        assert "cat" not in result[0]
    assert len(results) == 1

    results = list(doc.search(LineRange(1, 1000), "rot", case_sensitive=False))
    for result in results:
        assert "rot" not in result[0]
    assert len(results) == 3

    results = list(doc.search(LineRange(1, 1000), "rOT", case_sensitive=False))
    for result in results:
        assert "rOT" not in result[0]
    assert len(results) == 3

from dedlin.basic_types import LineRange
from dedlin.document import Document
from tests.fakes import fake_edit, fake_input


def test_document_copy():
    lines = ["cats", "dogs"]
    doc = Document(fake_input, fake_edit, lines)

    doc.copy(LineRange(1, 1), 2)
    assert doc.lines == ["cats", "cats", "dogs"]


def test_document_move_front_stuff_to_back():
    lines = ["1", "2", "3", "4"]
    doc = Document(fake_input, fake_edit, lines)

    doc.move(LineRange(1, 2), 4)
    assert doc.lines == [
        "3",
        "4",
        "1",
        "2",
    ]


def test_document_move_back_stuff_to_front():
    lines = ["1", "2", "3", "4"]
    doc = Document(fake_input, fake_edit, lines)

    doc.move(LineRange(3, 4), 1)
    assert doc.lines == [
        "3",
        "4",
        "1",
        "2",
    ]
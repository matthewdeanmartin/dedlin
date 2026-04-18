from dedlin.basic_types import LineRange
from dedlin.document import Document
from tests.fakes import fake_edit, fake_input


def test_document_copy():
    lines = ["cats", "dogs"]
    doc = Document(fake_input, fake_edit, lines)

    doc.copy(LineRange(1, 0), 2)
    assert doc.lines == ["cats", "cats", "dogs"]


def test_document_move_front_stuff_to_back():
    lines = ["1", "2", "3", "4"]
    doc = Document(fake_input, fake_edit, lines)

    # move lines 1-2 (1, 1) to before line 4
    doc.move(LineRange(1, 1), 4)
    assert doc.lines == [
        "3",
        "1",
        "2",
        "4",
    ]


def test_document_move_front_stuff_to_back_2():
    lines = ["1", "2", "3", "4", "", "", ""]
    doc = Document(fake_input, fake_edit, lines)

    # move lines 1-3 (1, 2) to before line 5
    doc.move(LineRange(1, 2), 5)
    assert doc.lines == ["4", "1", "2", "3", "", "", ""]


def test_document_move_back_stuff_to_front():
    lines = ["1", "2", "3", "4"]
    doc = Document(fake_input, fake_edit, lines)

    # move lines 3-4 (3, 1) to before line 1
    doc.move(LineRange(3, 1), 1)
    assert doc.lines == [
        "3",
        "4",
        "1",
        "2",
    ]

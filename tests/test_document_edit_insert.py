from dedlin.basic_types import LineRange
from dedlin.document import Document
from tests.fakes import fake_edit, fake_input


def test_document_edit():
    lines = ["aaa", "bbb"]
    doc = Document(fake_input, fake_edit, lines)

    doc.edit(1)
    assert doc.lines[0] == fake_edit("", "") + "\n"


def test_document_insert():
    lines = ["1", "2", "3", "4"]
    doc = Document(fake_input, fake_edit, lines)

    doc.insert(2)
    assert doc.lines == ["1", "cat\n", "dog\n", "2", "3", "4"]

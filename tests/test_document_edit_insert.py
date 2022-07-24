from dedlin.basic_types import LineRange
from dedlin.document import Document
from dedlin.document_sources import InMemoryInputter


def test_document_edit():
    lines = ["aaa", "bbb"]
    fake_input = InMemoryInputter(lines)
    fake_edit = InMemoryInputter([])
    doc = Document(fake_input, fake_edit, lines)

    doc.edit(1)
    assert doc.lines


def test_document_insert():
    lines = (_ for _ in ("1", "2", "3", "4"))
    new_lines = (_ for _ in ("cat", "dog"))
    fake_input = InMemoryInputter(new_lines)
    fake_edit = InMemoryInputter([])
    doc = Document(fake_input, fake_edit, list(lines))

    doc.insert(2)
    assert doc.lines == ["1", "cat", "dog", "2", "3", "4"]

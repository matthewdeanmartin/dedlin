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


def test_document_delete_first():
    lines = ["aaa", "bbb"]
    fake_input = InMemoryInputter(lines)
    fake_edit = InMemoryInputter([])
    doc = Document(fake_input, fake_edit, lines)

    doc.delete(LineRange(1, offset=0))
    assert len(doc.lines) == 1
    assert doc.lines[0] == "bbb"


def test_document_delete_all():
    lines = ["aaa", "bbb"]
    fake_input = InMemoryInputter(lines)
    fake_edit = InMemoryInputter([])
    doc = Document(fake_input, fake_edit, lines)

    doc.delete()
    assert len(doc.lines) == 0


def test_document_delete_last():
    lines = ["aaa", "bbb"]
    fake_input = InMemoryInputter(lines)
    fake_edit = InMemoryInputter([])
    doc = Document(fake_input, fake_edit, lines)

    doc.delete(LineRange(2, offset=0))
    assert len(doc.lines) == 1


def test_document_delete_middle():
    lines = ["aaa", "bbb", "ccc", "ddd"]
    fake_input = InMemoryInputter(lines)
    fake_edit = InMemoryInputter([])
    doc = Document(fake_input, fake_edit, lines)

    doc.delete(LineRange(2, offset=1))
    assert len(doc.lines) == 2
    assert doc.lines == ["aaa", "ddd"]


def test_document_replace():
    lines = ["the rain in spain falls mainly on the plain", "but the snow in idaho falls mainly on the mountain"]
    fake_input = InMemoryInputter(lines)
    fake_edit = InMemoryInputter([])
    doc = Document(fake_input, fake_edit, lines)

    result = list(doc.replace(LineRange(2, offset=1), target="snow", replacement="ice"))
    assert "but the ice in idaho falls mainly on the mountain" in result[0]
    assert len(result) == 1

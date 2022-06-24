from hypothesis import given
from hypothesis.strategies import text, integers

from dedlin.document import Document
from tests.fakes import fake_input, fake_edit


@given(integers(min_value=0,
    max_value=1000000,
))
def test_document_insert_anywhere(value:int)->None:
    lines = []
    doc = Document(fake_input, fake_edit, lines)
    doc.insert(value)
    assert doc.lines

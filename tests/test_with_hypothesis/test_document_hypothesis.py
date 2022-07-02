from hypothesis import given
from hypothesis.strategies import integers, text

from dedlin.document import Document
from tests.fakes import fake_edit, fake_input

# @given(
#     integers(
#         min_value=0,
#         max_value=0,
#     )
# )
# def test_document_insert_anywhere(value: int) -> None:
#     lines = []
#     doc = Document(fake_input,
#
#                    fake_edit, lines)
#     doc.insert(value)
#     assert doc.lines

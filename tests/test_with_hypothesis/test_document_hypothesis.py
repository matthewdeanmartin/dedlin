from hypothesis import given
from hypothesis import strategies as st

import dedlin.document


@given(
    start=st.integers(min_value=1, max_value=5),
    offset=st.integers(min_value=0, max_value=10),
    repeat=st.integers(min_value=1),
)
def test_fuzz_LineRange(start, offset, repeat):
    result = dedlin.document.LineRange(start=start, offset=offset, repeat=repeat)
    result.format()
    assert result.validate()


@given(parts=st.tuples(st.text(), st.text()))
def test_fuzz_Phrases(parts):
    result = dedlin.document.Phrases(parts=parts)
    result.format()
    # assert result.validate()


# Hangs?
# @given(line=st.text())
# def test_fuzz_check(line):
#     dedlin.document.check(line=line)

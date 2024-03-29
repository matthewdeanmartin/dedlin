from hypothesis import given
from hypothesis import strategies as st

import dedlin.document


@given(start=st.integers(min_value=1), offset=st.integers(min_value=0), repeat=st.integers(min_value=0))
def test_fuzz_LineRange(start, offset, repeat):
    dedlin.document.LineRange(start=start, offset=offset, repeat=repeat)


# Hangs
# @given(line=st.text())
# def test_fuzz_check(line):
#     dedlin.document.check(line=line)

import typing

from hypothesis import given
from hypothesis import strategies as st

import dedlin.document


@given(start=st.integers(), end=st.integers(), repeat=st.integers())
def test_fuzz_LineRange(start, end, repeat):
    dedlin.document.LineRange(start=start, end=end, repeat=repeat)


#
# @given(line=st.text())
# def test_fuzz_check(line):
#     dedlin.document.check(line=line)

from hypothesis import given
from hypothesis import strategies as st

import dedlin.document


@given(
    start=st.integers(min_value=1, max_value=5),
    end=st.integers(min_value=5, max_value=10),
    repeat=st.integers(min_value=1),
)
def test_fuzz_LineRange(start, end, repeat):
    result = dedlin.document.LineRange(start=start, end=end, repeat=repeat)
    result.format()
    assert result.validate()


@given(
    first=st.text(),
    second=st.one_of(st.none(), st.text()),
    third=st.one_of(st.none(), st.text()),
    fourth=st.one_of(st.none(), st.text()),
    fifth=st.one_of(st.none(), st.text()),
)
def test_fuzz_Phrases(first, second, third, fourth, fifth):
    result = dedlin.document.Phrases(first=first, second=second, third=third, fourth=fourth, fifth=fifth)
    result.format()
    # assert result.validate()


# Hangs?
# @given(line=st.text())
# def test_fuzz_check(line):
#     dedlin.document.check(line=line)

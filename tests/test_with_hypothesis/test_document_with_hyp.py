import typing

from hypothesis import given
from hypothesis import strategies as st

import dedlin.document


@given(
    inputter=st.from_type(typing.Callable[[int], typing.Generator[typing.Optional[str], None, None]]),
    editor=st.functions(like=lambda *a, **k: None, returns=st.text()),
    lines=st.lists(st.text()),
)
def test_fuzz_Document(inputter, editor, lines):
    dedlin.document.Document(inputter=inputter, editor=editor, lines=lines)


@given(start=st.integers(), end=st.integers(), repeat=st.integers())
def test_fuzz_LineRange(start, end, repeat):
    dedlin.document.LineRange(start=start, end=end, repeat=repeat)


@given(line=st.text())
def test_fuzz_check(line):
    dedlin.document.check(line=line)

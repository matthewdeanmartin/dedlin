# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

from hypothesis import given
from hypothesis import strategies as st

import dedlin.basic_types
from dedlin.basic_types import LineRange, Phrases

# TODO: replace st.nothing() with an appropriate strategy


@given(
    command=st.sampled_from(dedlin.basic_types.Commands),
    line_range=st.one_of(
        st.none(),
        st.builds(
            LineRange,
            start=st.integers(1),
            offset=st.integers(0),
            repeat=st.one_of(st.just(1), st.integers(min_value=0)),
        ),
    ),
    phrases=st.one_of(
        st.none(),
        st.builds(Phrases, parts=st.tuples(st.text(), st.text())),
    ),
    original_text=st.one_of(st.none(), st.text()),
)
def test_fuzz_Command(command, line_range, phrases, original_text):
    command = dedlin.basic_types.Command(
        command=command,
        line_range=line_range,
        phrases=phrases,
        original_text=original_text,
    )
    assert command.validate()


@given(
    start=st.integers(min_value=1, max_value=10),
    offset=st.integers(min_value=1, max_value=20),
    repeat=st.integers(min_value=1),
)
def test_fuzz_LineRange(start, offset, repeat):
    line_range = dedlin.basic_types.LineRange(start=start, offset=offset, repeat=repeat)
    assert line_range.validate()


@given(start=st.integers(min_value=1), repeat=st.integers(min_value=1))
def test_fuzz_LineRange_one_point_range(start, repeat):
    line_range = dedlin.basic_types.LineRange(start=start, offset=0, repeat=repeat)
    assert line_range.validate()


@given(
    parts=st.tuples(st.text(), st.text()),
)
def test_fuzz_Phrases(parts):
    dedlin.basic_types.Phrases(parts=parts)


@given(value=st.text(), default_value=st.one_of(st.none(), st.integers()))
def test_fuzz_try_parse_int(value, default_value):
    dedlin.basic_types.try_parse_int(value=value, default_value=default_value)

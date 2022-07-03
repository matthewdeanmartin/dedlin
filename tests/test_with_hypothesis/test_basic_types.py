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
            start=st.integers(1, 5),
            end=st.integers(5, 6),
            repeat=st.one_of(st.just(1), st.integers(min_value=1)),
        ),
    ),
    phrases=st.one_of(
        st.none(),
        st.builds(
            Phrases,
            fifth=st.one_of(st.none(), st.one_of(st.none(), st.text())),
            fourth=st.one_of(st.none(), st.one_of(st.none(), st.text())),
            second=st.one_of(st.none(), st.one_of(st.none(), st.text())),
            third=st.one_of(st.none(), st.one_of(st.none(), st.text())),
        ),
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
    end=st.integers(min_value=10, max_value=20),
    repeat=st.integers(min_value=1),
)
def test_fuzz_LineRange(start, end, repeat):
    line_range = dedlin.basic_types.LineRange(start=start, end=end, repeat=repeat)
    assert line_range.validate()


@given(start=st.integers(min_value=1), repeat=st.integers(min_value=1))
def test_fuzz_LineRange_one_point_range(start, repeat):
    line_range = dedlin.basic_types.LineRange(start=start, end=start, repeat=repeat)
    assert line_range.validate()


@given(
    first=st.text(),
    second=st.one_of(st.none(), st.text()),
    third=st.one_of(st.none(), st.text()),
    fourth=st.one_of(st.none(), st.text()),
    fifth=st.one_of(st.none(), st.text()),
)
def test_fuzz_Phrases(first, second, third, fourth, fifth):
    dedlin.basic_types.Phrases(first=first, second=second, third=third, fourth=fourth, fifth=fifth)


@given(value=st.text(), default_value=st.one_of(st.none(), st.integers()))
def test_fuzz_try_parse_int(value, default_value):
    dedlin.basic_types.try_parse_int(value=value, default_value=default_value)

from hypothesis import given
from hypothesis import strategies as st
from hypothesis.strategies import builds, integers, text

from dedlin.basic_types import LineRange, Phrases


@given(integers(min_value=1), integers(min_value=0), integers(min_value=0))
def test_create_With_any_integer(start, offset, repeat):
    range = LineRange(start, offset, repeat)
    assert range


@given(integers(min_value=1, max_value=5), integers(min_value=0, max_value=20), integers(min_value=0))
def test_validate_and_format_with_well_behaved(start, offset, repeat):
    range = LineRange(start, offset, repeat)
    assert range.validate()
    assert range.format()


@given(builds(Phrases, parts=st.tuples(text(), text())))
def test_phrases(phrases: Phrases):
    if phrases.parts and any(phrases.parts):
        # empty list and no truthy elements
        assert phrases.format()
        assert phrases.as_list()

    if phrases.parts and not any(phrases.parts):
        assert not phrases.format()
        assert phrases.as_list()

    if not phrases.parts:
        # empty list
        assert not phrases.format()
        assert not phrases.as_list()

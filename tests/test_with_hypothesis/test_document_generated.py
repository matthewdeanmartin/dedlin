from hypothesis import given
from hypothesis.strategies import builds, integers, text

from dedlin.basic_types import LineRange, Phrases


@given(integers(), integers(), integers())
def test_create_With_any_integer(start, end, repeat):
    range = LineRange(start, end, repeat)
    assert range


@given(integers(min_value=1, max_value=5), integers(min_value=5, max_value=20), integers(min_value=0))
def test_validate_and_format_with_well_behaved(start, end, repeat):
    range = LineRange(start, end, repeat)
    assert range.validate()
    assert range.format()


@given(builds(Phrases, text(min_size=1), text()))
def test_phrases(phrases):
    assert phrases.format()
    assert phrases.as_list()

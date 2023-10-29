import pytest
from pydantic import ValidationError

from dedlin.basic_types import LineRange, Phrases, try_parse_int


def test_line_range_validate():
    line_range = LineRange(1, 1)
    assert line_range.validate()

    with pytest.raises(ValidationError):
        line_range = LineRange(-1, 2)
        assert not line_range.validate()

    with pytest.raises(ValidationError):
        line_range = LineRange(3, -2)
        assert not line_range.validate()


def test_line_range_validate_with_repeats():
    line_range = LineRange(1, 3, 1)
    assert line_range.validate()

    line_range = LineRange(1, 3, 0)
    assert line_range.validate()

    # with pytest.raises(ValidationError):
    line_range = LineRange(1, 3, -1)
    assert not line_range.validate()


def test_line_range_format():
    line_range = LineRange(1, 1)
    assert line_range.format() == "1,2"

    line_range = LineRange(1, 0)
    assert line_range.format() == "1"

    line_range = LineRange(1, 1, 3)
    assert line_range.format() == "1,2,3"


def test_try_parse_int():
    assert try_parse_int("1") == 1
    assert try_parse_int("asdf") is None
    assert try_parse_int("asdf", default_value=1) == 1


def test_line_range_slice():
    line_range = LineRange(1, offset=0)
    assert line_range.start == 1
    assert line_range.end == 1
    assert [1, 2, 3, 4, 5][line_range.to_slice()] == [1]

    line_range = LineRange(1, offset=1)
    assert line_range.start == 1
    assert line_range.end == 2
    assert [1, 2, 3, 4, 5][line_range.to_slice()] == [1, 2]

    line_range = LineRange(2, offset=2)
    assert line_range.start == 2
    assert line_range.end == 4
    assert [1, 2, 3, 4, 5][line_range.to_slice()] == [2, 3, 4]

    line_range = LineRange(1, offset=4)
    assert line_range.start == 1
    assert line_range.end == 5
    assert [1, 2, 3, 4, 5][line_range.to_slice()] == [1, 2, 3, 4, 5]

    line_range = LineRange(3, offset=1)
    assert line_range.start == 3
    assert line_range.end == 4
    assert [1, 2, 3, 4, 5][line_range.to_slice()] == [3, 4]


def test_phrases_parts():
    phrases = Phrases(parts=("a", "b", "c", "d", "e", "f"))
    assert phrases.first == "a"
    assert phrases.second == "b"
    assert phrases.third == "c"
    assert phrases.fourth == "d"
    assert phrases.fifth == "e"
    assert phrases.sixth == "f"


def test_phrases_quotes():
    phrases = Phrases(parts=("'a'", "'b'", "'c'", "'d'", "'e'", "'f'"))
    assert phrases.format() == "'a' 'b' 'c' 'd' 'e' 'f'"

    # does this make sense? maybe not.
    phrases = Phrases(parts=("'a a'", "'b b'", "'c c'", "'d d'", "'e e'", "'f f'"))
    assert phrases.format() == "\"'a a'\" \"'b b'\" \"'c c'\" \"'d d'\" \"'e e'\" \"'f f'\""
    phrases = Phrases(parts=('"a a"', '"b b"', '"c c"', '"d d"', '"e e"', '"f f"'))
    assert phrases.format() == '"\\"a a\\" "\\"b b\\" "\\"c c\\" "\\"d d\\" "\\"e e\\" "\\"f f\\"'

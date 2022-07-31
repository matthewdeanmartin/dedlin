import pytest
from pydantic import ValidationError

from dedlin.basic_types import LineRange, try_parse_int


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
    line_range = LineRange(1, 1)
    assert [1, 2, 3, 4, 5][line_range.to_slice()] == [1]

    line_range = LineRange(1, 2)
    assert [1, 2, 3, 4, 5][line_range.to_slice()] == [1, 2]

    line_range = LineRange(2, 3)
    assert [1, 2, 3, 4, 5][line_range.to_slice()] == [2, 3, 4]

    line_range = LineRange(1, 5)
    assert [1, 2, 3, 4, 5][line_range.to_slice()] == [1, 2, 3, 4, 5]

    line_range = LineRange(3, 2)
    assert [1, 2, 3, 4, 5][line_range.to_slice()] == [3, 4]

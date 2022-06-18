from dedlin.basic_types import LineRange


def test_line_range():
    line_range = LineRange(1, 2)
    assert line_range.validate()

    line_range = LineRange(-1, 2)
    assert not line_range.validate()

    line_range = LineRange(3, 1)
    assert not line_range.validate()

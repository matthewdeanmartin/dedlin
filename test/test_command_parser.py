from dedlin.basic_types import LineRange
from dedlin.main import extract_one_range, parse_command, Commands


def test_extract_one_range():
    assert extract_one_range("1") == LineRange(start=1, end=1)
    assert extract_one_range("2,2") == LineRange(start=2, end=2)
    assert extract_one_range("1,2") == LineRange(start=1, end=2)


def test_parse_command_insert():
    for insert in ("I", "Insert", "insert", "i", "INSERT"):
        assert parse_command(insert, 3) == (Commands.Insert, -1), insert
        assert parse_command(f"2{insert}", 3) == (Commands.Insert, 2), f"2{insert}"
        assert parse_command(f"2 {insert}", 3) == (Commands.Insert, 2), f"2 {insert}"


def test_parse_command_edit():
    assert parse_command("1", 3) == (Commands.Edit, 1)
    assert parse_command("2", 3) == (Commands.Edit, 2)
    assert parse_command("3", 3) == (Commands.Edit, 3)

    # for edit in ("E", "Edit", "edit", "e", "EDIT"):
    # assert parse_command(f"1{edit}", 3) == (Commands.Edit, 1), f"1{edit}"
    # assert parse_command(f"1 {edit}", 3) == (Commands.Edit, 1), f"1 {edit}"


def test_parse_command_delete():
    assert parse_command("D", 3) == (Commands.Delete, LineRange(start=1, end=3))
    for edit in ("D", "Delete", "delete", "d", "DELETE"):
        assert parse_command(f"1{edit}", 3) == (Commands.Delete, LineRange(start=1, end=1)), f"1{edit}"
        assert parse_command(f"1 {edit}", 3) == (Commands.Delete, LineRange(start=1, end=1)), f"1 {edit}"
        assert parse_command(f"1,2 {edit}", 3) == (Commands.Delete, LineRange(start=1, end=2)), f"1,2 {edit}"
        assert parse_command(f"1,2{edit}", 3) == (Commands.Delete, LineRange(start=1, end=2)), f"1,2{edit}"
#
# def test_trouble():
#     edit = "DELETE"
#     assert parse_command(f"1{edit}", 3) == (Commands.Delete, LineRange(start=1, end=1)), f"1{edit}"
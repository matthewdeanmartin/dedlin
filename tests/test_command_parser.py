from dedlin.basic_types import Command, LineRange, Phrases
from dedlin.main import Commands, parse_command
from dedlin.parsers import extract_one_range, extract_phrases


def test_extract_one_range():
    assert extract_one_range("1", 1, 1) == LineRange(start=1, end=1)
    assert extract_one_range("2,2", 1, 2) == LineRange(start=2, end=2)
    assert extract_one_range("1,2", 1, 2) == LineRange(start=1, end=2)


def test_parse_command_insert_default():

    for insert in ("I", "Insert", "insert", "i", "INSERT"):
        assert parse_command(insert, 1, 3) == Command(
            Commands.INSERT,  # LineRange(start=1, end=1), # Phrases("")
        ), insert


def test_parse_command_insert_specific_rage():

    for insert in ("I", "Insert", "insert", "i", "INSERT"):

        assert parse_command(f"2{insert}", 1, 3) == Command(
            Commands.INSERT,
            LineRange(start=2, end=2),  # Phrases("")
        ), f"2{insert}"
        assert parse_command(f"2 {insert}", 1, 3) == Command(
            Commands.INSERT,
            LineRange(start=2, end=2),  # Phrases("")
        ), f"2 {insert}"


def test_parse_command_edit():
    assert parse_command("1", 1, 3) == Command(Commands.EDIT, LineRange(start=1, end=1))
    assert parse_command("2", 1, 3) == Command(Commands.EDIT, LineRange(start=2, end=2))
    assert parse_command("3", 1, 3) == Command(Commands.EDIT, LineRange(start=3, end=3))

    # for edit in ("E", "Edit", "edit", "e", "EDIT"):
    # assert parse_command(f"1{edit}", 3) == (Commands.Edit, 1), f"1{edit}"
    # assert parse_command(f"1 {edit}", 3) == (Commands.Edit, 1), f"1 {edit}"


def test_parse_command_delete():
    assert parse_command("D", 1, 3) == Command(Commands.DELETE, LineRange(start=1, end=3))
    for edit in ("D", "Delete", "delete", "d", "DELETE"):
        assert parse_command(f"1{edit}", 1, 3) == Command(Commands.DELETE, LineRange(start=1, end=1)), f"1{edit}"
        assert parse_command(f"1 {edit}", 1, 3) == Command(Commands.DELETE, LineRange(start=1, end=1)), f"1 {edit}"
        assert parse_command(f"1,2 {edit}", 1, 3) == Command(Commands.DELETE, LineRange(start=1, end=2)), f"1,2 {edit}"
        assert parse_command(f"1,2{edit}", 1, 3) == Command(Commands.DELETE, LineRange(start=1, end=2)), f"1,2{edit}"


def test_parse_phrases_space_delimited():
    assert extract_phrases("cat dog") == Phrases(first="cat", second="dog")


def test_parse_phrases_quoted():
    assert extract_phrases('"cat frog" "log dog"') == Phrases(first="cat frog", second="log dog")


def test_phrases_format():
    thing = Phrases(first="cat frog", second="log dog")
    result = thing.format()
    assert result == '"cat frog" "log dog"'

    thing = Phrases(first="cat", second="log")
    result = thing.format()
    assert result == "cat log"


def test_parse_extract_phrases():
    assert extract_phrases("cat") == Phrases(first="cat")

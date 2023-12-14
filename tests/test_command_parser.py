from dedlin.basic_types import Command, LineRange, Phrases
from dedlin.main import Commands
from dedlin.parsers import extract_one_range, extract_phrases, parse_command


def test_extract_one_range():
    assert extract_one_range("1", 1, 1) == LineRange(start=1, offset=0)
    assert extract_one_range("2,2", 1, 2) == LineRange(start=2, offset=0)
    assert extract_one_range("1,2", 1, 2) == LineRange(start=1, offset=1)


def test_parse_command_insert_default():
    for insert in ("I", "Insert", "insert", "i", "INSERT"):
        assert parse_command(insert, 1, 3, headless=False) == Command(
            Commands.INSERT, LineRange(start=1, offset=2), None
        ), insert


def test_parse_copy():
    command = "2,3 copy 1"
    result = parse_command(command, 1, 5, headless=False)
    assert result.command == Commands.COPY


def test_parse_move():
    command = "2,3 move 1"
    result = parse_command(command, 1, 5, headless=False)
    assert result.command == Commands.MOVE


def test_parse_command_insert_specific_rage():
    for insert in ("I", "Insert", "insert", "i", "INSERT"):
        assert parse_command(f"2{insert}", 1, 3, headless=False) == Command(
            Commands.INSERT,
            LineRange(start=2, offset=0),  # Phrases("")
        ), f"2{insert}"
        assert parse_command(f"2 {insert}", 1, 3, headless=False) == Command(
            Commands.INSERT,
            LineRange(start=2, offset=0),  # Phrases("")
        ), f"2 {insert}"


def test_parse_command_edit():
    assert parse_command("1", 1, 3, headless=False) == Command(Commands.EDIT, LineRange(start=1, offset=0))
    assert parse_command("2", 1, 3, headless=False) == Command(Commands.EDIT, LineRange(start=2, offset=0))
    assert parse_command("3", 1, 3, headless=False) == Command(Commands.EDIT, LineRange(start=3, offset=0))

    # for edit in ("E", "Edit", "edit", "e", "EDIT"):
    # assert parse_command(f"1{edit}", 3) == (Commands.Edit, 1), f"1{edit}"
    # assert parse_command(f"1 {edit}", 3) == (Commands.Edit, 1), f"1 {edit}"


def test_parse_command_delete():
    assert parse_command("D", 1, 3, headless=False) == Command(Commands.DELETE, LineRange(start=1, offset=2))
    for edit in ("D", "Delete", "delete", "d", "DELETE"):
        assert parse_command(f"1{edit}", 1, 3, headless=False) == Command(
            Commands.DELETE, LineRange(start=1, offset=0)
        ), f"1{edit}"
        assert parse_command(f"1 {edit}", 1, 3, headless=False) == Command(
            Commands.DELETE, LineRange(start=1, offset=0)
        ), f"1 {edit}"
        assert parse_command(f"1,2 {edit}", 1, 3, headless=False) == Command(
            Commands.DELETE, LineRange(start=1, offset=1)
        ), f"1,2 {edit}"
        assert parse_command(f"1,2{edit}", 1, 3, headless=False) == Command(
            Commands.DELETE, LineRange(start=1, offset=1)
        ), f"1,2{edit}"


def test_parse_phrases_space_delimited():
    assert extract_phrases("cat dog") == Phrases(["cat", "dog"])


def test_parse_phrases_quoted():
    assert extract_phrases('"cat frog" "log dog"') == Phrases(["cat frog", "log dog"])


def test_phrases_format():
    thing = Phrases(["cat frog", "log dog"])
    result = thing.format()
    assert result == '"cat frog" "log dog"'

    thing = Phrases(["cat", "log"])
    result = thing.format()
    assert result == "cat log"


def test_parse_extract_phrases():
    assert extract_phrases("cat") == Phrases(["cat"])


def test_parse_upper():
    command = "1,2 upper"
    result = parse_command(command, 1, 20, headless=False)
    assert result.command == Commands.UPPER


def test_parse_list():
    command = "1,2 LIST"
    result = parse_command(command, 1, 20, headless=False)
    assert result.command == Commands.LIST


def test_parse_upper_spaceless():
    command = "1,2upper"
    result = parse_command(command, 1, 20, headless=False)
    assert result.command == Commands.UPPER

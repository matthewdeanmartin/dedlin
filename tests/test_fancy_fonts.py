from dedlin.flash import title_screen


def test_title_screen(capsys) -> None:
    title_screen()
    captured = capsys.readouterr()
    assert "\n" in captured.out

from dedlin.flash import title_screen


def test_title_screen(capsys) -> None:
    title_screen(user_is_blind=False)
    captured = capsys.readouterr()
    assert "\n" in captured.out


def test_title_screen_blind(capsys) -> None:
    title_screen(user_is_blind=True)
    captured = capsys.readouterr()
    assert captured.out == ""

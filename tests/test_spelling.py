from dedlin.spelling_overlay import check


def test_spellcheck():
    line = "So it goes and 'what' and then the other So! wow. rieciept and cieling."
    print(line)
    result = check(line)
    assert "id you mean ceiling?" in result

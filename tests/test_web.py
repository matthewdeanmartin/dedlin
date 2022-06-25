from dedlin.web import fetch_page_as_rows

def test_fetch_page_as_rows():
    result = fetch_page_as_rows("https://github.com/matthewdeanmartin/dedlin")
    found = False
    for item in result:
        found = True
        break
    assert found

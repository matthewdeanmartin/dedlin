"""Cover tools/export.py.

This module had no test coverage at all, which is why a real break went unnoticed:
Python 3.15 made re.Scanner reject capturing groups, so every mistune 2.x release
raises at parse time and export_markdown() was dead on 3.15 while the suite stayed
green. These tests exercise the renderer so that cannot happen silently again.
"""

from __future__ import annotations

from dedlin.tools.export import export_markdown


def test_export_markdown_renders_basic_html():
    """The happy path actually invokes mistune, so an unusable mistune fails here."""
    result = export_markdown(["# Title", "", "Some text."], "\n")
    assert "<h1>Title</h1>" in result
    assert "<p>Some text.</p>" in result


def test_export_markdown_renders_inline_markup_and_lists():
    """Covers the constructs whose HTML differs most between mistune versions."""
    result = export_markdown(["Some *text* and a [link](http://x).", "", "- a", "- b"], "\n")
    assert "<em>text</em>" in result
    assert '<a href="http://x">link</a>' in result
    assert "<li>a</li>" in result
    assert "<li>b</li>" in result


def test_export_markdown_honours_the_line_break():
    """The joiner is the caller's, not hardcoded."""
    assert "<h1>Title</h1>" in export_markdown(["# Title", "", "text"], "\r\n")


def test_export_markdown_handles_empty_input():
    assert export_markdown([], "\n").strip() == ""

"""Primative printing support"""
from pathlib import Path

from markdown_it import MarkdownIt

# Support these?
# from mdit_py_plugins.front_matter import front_matter_plugin
# from mdit_py_plugins.footnote import footnote_plugin


def write_to_markdown(filename: str, lines: list[str]) -> str:
    """Write to html if markdown.

    Args:
        filename (str): The filename
        lines (list[str]): The lines

    Returns:
        str: The html
    """
    md = (
        MarkdownIt("commonmark", {"breaks": True, "html": True})
        # .use(front_matter_plugin)
        # .use(footnote_plugin)
        .enable("table")
    )
    html_text = md.render("\n".join(lines))
    path = Path(filename)
    if path.suffix == ".md":
        path.rename(path.with_suffix(".html"))
        path.write_text(html_text, encoding="utf-8")
    else:
        print("Not markdown!")
    return html_text

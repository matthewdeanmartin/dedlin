"""
Export to file formats, particularly markdown
"""
import mistune


def export_markdown(lines: list[str], preferred_line_break: str) -> str:
    """Write to file.

    Args:
        lines (list[str]): The lines
        preferred_line_break (str): The preferred line break
    Returns:
        str: The markdown
    """
    markdown = mistune.create_markdown()
    return markdown(preferred_line_break.join(lines))

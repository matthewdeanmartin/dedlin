"""Metadata for dedlin."""

__all__ = [
    "__credits__",
    "__dependencies__",
    "__description__",
    "__keywords__",
    "__readme__",
    "__requires_python__",
    "__status__",
    "__title__",
    "__version__",
]

__title__ = "dedlin"
__version__ = "1.20.0"
__description__ = "Line editor, edlin clone with many improvements"
__credits__ = [{"name": "Matthew Martin", "email": "matthewdeanmartin@gmail.com"}]
__readme__ = "README.md"
__requires_python__ = ">=3.14"
__keywords__ = ["editor", "edlin", "line editor"]
__status__ = "4 - Beta"
__dependencies__ = [
    "questionary>=2.0.1",
    "rich>=13.7.0",
    "icontract>=2.6.4",
    "pydantic>2.5.0",
    "pyspellchecker>=0.7.2",
    "textstat>=0.7.3,<1",
    "pygments>=2.16.1",
    "html2text>=2020.1.16",
    "requests>=2.31.0",
    "art>=6.1",
    "mistune<3.0.0; python_version < '3.15'",
    "mistune>=3.1.4; python_version >= '3.15'",
    "markdown-it-py>=3.0.0",
    "pywin32>=228; sys_platform == 'win32'",
]

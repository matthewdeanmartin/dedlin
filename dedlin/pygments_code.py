"""
Attempt to make basic syntax highlighting work for the dedlin DSL.
"""
from pygments.lexer import RegexLexer
from pygments.token import Comment, Keyword, Text


class EdLexer(RegexLexer):
    name = "ED"
    aliases = ["ed"]
    filenames = ["*.ed"]

    tokens = {
        "root": [
            (r"\s+", Text),
            (r"#.*?$", Comment),
            (r"INSERT|DELETE|PAGE|LIST$", Keyword),
            # (r'(.*?)(\s*)(=)(\s*)(.*?)$',
            #  bygroups(Name.Attribute, Text, Operator, Text, String))
        ]
    }

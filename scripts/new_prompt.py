from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.lexers import guess_lexer_for_filename
from pygments.styles import get_style_by_name

# from prompt_toolkit.formatted_text import HTML

thing = guess_lexer_for_filename("cats.py", "")
style = style_from_pygments_cls(get_style_by_name("monokai"))

# Create prompt object.
session = PromptSession(
    history=InMemoryHistory(),
)

while True:
    text = session.prompt(
        "Enter HTML: ",
        # lexer=thing, # PygmentsLexer(),
        style=style,
        default="def main():",
        include_default_pygments_style=False,
        enable_history_search=True,
    )
    print(text)
    # yield text

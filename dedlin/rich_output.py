from rich.console import Console
from rich.syntax import Syntax

my_code = '''
def iter_first_last(values: Iterable[T]) -> Iterable[Tuple[bool, bool, T]]:
    """Iterate and generate a tuple with a flag for first and last value."""
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)
    except StopIteration:
        return
    first = True
    for value in iter_values:
        yield first, False, previous_value
        first = False
        previous_value = value
    yield first, True, previous_value
'''


class RichPrinter:
    def __init__(self):
        self.console = Console()

    def print(self, text, end):
        if text and text.endswith("\n"):
            text = text[:-1]
        syntax = Syntax(text, "python", theme="monokai", line_numbers=False)
        self.console.print(syntax, end="")

"""
Dedlin is an edlin clone with additional features. Possibly useful as a sed-like DSL or as an editor
for AI function calls.
"""
from dedlin.command_sources import (
    CommandGenerator,
    InteractiveGenerator,
    StringCommandGenerator,
)
from dedlin.document_sources import PrefillInputter, SimpleInputter, input_with_prefill
from dedlin.flash import title_screen
from dedlin.logging_utils import configure_logging
from dedlin.main import Dedlin
from dedlin.outputters import rich_output, talking_outputter
from dedlin.outputters.plain import plain_printer

# All the parts necessary to implement an alternative to __main__
__all__ = [
    "CommandGenerator",
    "InteractiveGenerator",
    "StringCommandGenerator",
    "PrefillInputter",
    "SimpleInputter",
    "input_with_prefill",
    "title_screen",
    "configure_logging",
    "Dedlin",
    "rich_output",
    "talking_outputter",
    "plain_printer",
]

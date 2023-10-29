import dedlin.main as main_module
from dedlin.basic_types import Command, Commands, LineRange
from dedlin.command_sources import InMemoryCommandGenerator
from dedlin.document_sources import InMemoryInputter, PrefillInputter


def test_main():
    commands = [
        # Command(Commands.INSERT, LineRange(start=1, offset=2), None),
        Command(Commands.LIST, LineRange(start=1, offset=2), None),
    ]
    lines = []
    commandGenerator = InMemoryCommandGenerator(commands)
    inputter = InMemoryInputter(lines)
    thingy = {}

    app = main_module.Dedlin(
        inputter=commandGenerator, insert_document_inputter=inputter, edit_document_inputter=thingy, outputter=print
    )
    app.entry_point()

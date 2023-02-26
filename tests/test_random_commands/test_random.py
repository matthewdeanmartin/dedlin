from dedlin.basic_types import Command


def make_command(command: Command):
    yield command.format()


def test_go():
    pass

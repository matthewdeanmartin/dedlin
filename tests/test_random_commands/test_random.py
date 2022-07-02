from dedlin.basic_types import Command, LineRange
from dedlin.main import Dedlin


def make_command(command: Command):
    yield command.format()


def test_go():
    d = Dedlin

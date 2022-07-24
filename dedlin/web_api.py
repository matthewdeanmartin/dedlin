"""
If an app doesn't have a web API, does it even matter
"""
from dataclasses import field

import pydantic.dataclasses as dc
from fastapi import FastAPI

from dedlin.basic_types import Command
from dedlin.command_sources import InMemoryCommandGenerator
from dedlin.document_sources import InMemoryInputter
from dedlin.main import Dedlin
from dedlin.parsers import parse_command


@dc.dataclass
class InputPayload:
    commands: list[str] = field(default_factory=list)
    lines: list[str] = field(default_factory=list)


@dc.dataclass
class OutputPayload:
    messages: list[str] = field(default_factory=list)
    lines: list[str] = field(default_factory=list)


app = FastAPI()


@app.post("/execute")
async def execute(payload: InputPayload) -> OutputPayload:
    commands = []
    lines = payload.lines
    for command_text in payload.commands:
        candidate = parse_command(command_text, 0, document_length=len(lines))
        if candidate:
            commands.append(candidate)
    output = OutputPayload()
    output_lines = output.lines

    def outputter(value, _line_ending):
        output_lines.append(value)

    inputter = InMemoryCommandGenerator(commands)
    executor = Dedlin(
        inputter=inputter,
        insert_document_inputter=InMemoryInputter([]),
        edit_document_inputter=InMemoryInputter([]).generate,
        outputter=outputter,
    )
    executor.entry_point()
    return output
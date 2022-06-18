"""
Main code.

Handles UI and links command parser to the document object
"""
from pathlib import Path
from typing import Generator, Optional

import questionary

from dedlin.basic_types import Commands, Printable
from dedlin.document import Document
from dedlin.editable_input_prompt import input_with_prefill
from dedlin.parsers import parse_command

HELP_TEXT = """
Command format: [number],[number] [command] [parameter] [parameter]

Display Commands
[start],[end] List - display lines, set current to end of range
[start],[end] Page - repeat to flipt through entire document
[start],[end] Search [text]

Edit Commands
[line number] Insert - insert line at line number
[line number] Edit - edit number
[start],[end] Delete - delete range
[target] Transfer [file name] - inserts file contents to target
[start],[end] Replace "[text]", "[text]" - replace text in range

Reorder Commands
[start],[end] Move [target line number]
[start],[end] Copy [target line number]
[start],[end] Sort
[start],[end] Shuffle 

File System Commands
Quit
Exit [file name]

"""


def command_handler(prompt: str = "*") -> Generator[str, None, None]:
    """Wrapper around questionary for command input"""
    # possibly should merge with simple_input?
    while True:
        answer = questionary.text(prompt).ask()
        yield answer


def simple_input(start_line_number: int) -> Generator[str, None, None]:
    """Wrapper around questionary for insert"""
    line_number = start_line_number
    while True:
        prompt = f"   {line_number} : "
        response = questionary.text(prompt).ask(kbi_msg="Exiting insert mode")
        if response is None:
            break
        yield response
        line_number += 1


class Dedlin:
    """Application for Dedlin"""

    def __init__(self, inputter: Generator[str, None, None], outputter: Printable):
        """Set up inital state and some dependency injection"""
        self.inputter = inputter
        self.outputter = outputter
        self.doc: Optional[Document] = None
        self.halt_on_error = False
        self.echo = False

    def go(self, file_name: Optional[str] = None) -> int:
        """Entry point for Dedlin"""
        if file_name:
            path = Path(file_name)
            print(f"Editing {path.absolute()}")
            lines = read_file(path)
        else:
            path = None
            lines = []

        self.doc = Document(
            inputter=simple_input,
            editor=input_with_prefill,
            lines=lines,
            file_name=path,
        )
        while True:
            try:
                user_command_text = next(self.inputter)
            except StopIteration:
                break  # it on down now

            command = parse_command(
                user_command_text, document_length=len(self.doc.lines)
            )
            if command is None:
                self.outputter("Unknown command", end="\n")
                continue

            if self.echo:
                self.outputter(command.original_text)
            if command.command == Commands.Empty:
                pass
            elif command.command == Commands.List:
                for line in self.doc.list(command.line_range):
                    self.outputter(line, end="")
            elif command.command == Commands.Page:
                for line, end in self.doc.page():
                    self.outputter(line, end=end)
            elif command.command == Commands.Delete:
                self.doc.delete(command.line_range)
                self.outputter(
                    f"Deleted lines {command.line_range.start} to {command.line_range.end}"
                )
            elif command.command == Commands.Save:
                with open(path, "w", encoding="utf-8") as file:
                    file.writelines(self.doc.lines)
                return 0
            elif command.command == Commands.Quit:
                return 0
            elif command.command == Commands.Insert:
                line_number = command.line_range.start if command.line_range else 1
                self.outputter("Control C to exit edit mode")
                self.doc.insert(line_number)
            elif command.command == Commands.Edit:
                self.outputter("Control C to exit edit mode")
                line_number = command.line_range.start if command.line_range else 1
                self.doc.edit(line_number)
            elif command.command == Commands.Search:
                self.doc.search(command.line_range, value=command.phrases.first)
            elif command.command == Commands.Replace:
                self.outputter("Replacing")
                for line in self.doc.replace(
                    command.line_range,
                    target=command.phrases.first,
                    replacement=command.phrases.second,
                ):
                    self.outputter(line, end="")
            elif command.command == Commands.Lorem:
                self.doc.lorem(command.line_range)
            elif command.command == Commands.Undo:
                self.doc.undo()
                self.outputter("Undone")
            elif command.command == Commands.Sort:
                self.doc.sort()
                self.outputter("Sorted")
            elif command.command == Commands.Reverse:
                self.doc.reverse()
                self.outputter("Reversed")
            elif command.command == Commands.Shuffle:
                self.doc.shuffle()
                self.outputter("Shuffled")
            elif command.command == Commands.Empty:
                pass
            elif command.command == Commands.Help:
                self.outputter(HELP_TEXT)
            elif command.command == Commands.Unknown:
                self.outputter("Unknown command")
                self.outputter(HELP_TEXT)
                if self.halt_on_error:
                    raise Exception(f"Unknown command {user_command_text}")
            else:
                # possibly not reachable now.
                self.outputter(
                    "1i to insert at line 1.  E to save and quit. Q to just quit."
                )
        return 0


def read_file(path):
    """Read a file and return a list of lines"""
    lines: list[str] = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            if line.endswith("\n"):
                lines.append(line)
            else:
                lines.append(line + "\n")
    return lines


def run(file_name: Optional[str] = None):
    """Set up everything except things from command line"""
    dedlin = Dedlin(command_handler(), print)
    dedlin.go(file_name)


if __name__ == "__main__":
    run()

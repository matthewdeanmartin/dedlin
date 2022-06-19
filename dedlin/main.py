"""
Main code.

Handles UI and links command parser to the document object
"""
from pathlib import Path
from typing import Generator, Optional

import questionary

from dedlin.basic_types import Command, Commands, Printable
from dedlin.document import Document
from dedlin.editable_input_prompt import input_with_prefill
from dedlin.file_system import read_file, save_and_overwrite
from dedlin.help_text import HELP_TEXT
from dedlin.parsers import parse_command
from dedlin.rich_output import RichPrinter


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
        """Stop on errors, useful for macros."""

        self.quit_safety = True
        """Disable checking document.dirty on quit. Useful for unit tests."""

        self.echo = False
        self.file_path: Optional[Path] = None
        self.history: list[Command] = []

    def go(self, file_name: Optional[str] = None) -> int:
        """Entry point for Dedlin"""
        self.file_path = Path(file_name) if file_name else None
        lines = read_file(self.file_path)

        self.doc = Document(
            inputter=simple_input,
            editor=input_with_prefill,
            lines=lines,
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

            if not command.validate():
                self.outputter(f"Invalid command {command}")

            self.history.append(command)
            if command.command == Commands.Redo:
                command = self.history[-2]
                self.history.append(command)

            if self.echo:
                self.outputter(command.original_text)
            if command.command == Commands.History:
                for command in self.history:
                    self.outputter(command.original_text)
            elif command.command == Commands.Empty:
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
            elif command.command in (Commands.Exit, Commands.Quit, Commands.Save):
                if (
                        command.command == Commands.Quit
                        and self.doc.dirty
                        and self.quit_safety
                ):
                    # hack!
                    self.outputter("Save changes? (y/n) ", end="")
                    if next(self.inputter) == "y":
                        self.save_document()
                        return 0
                else:
                    self.save_document()
                if command.command in (Commands.Quit, Commands.Exit):
                    return 0
            elif command.command == Commands.Insert:
                line_number = command.line_range.start if command.line_range else 1
                self.outputter("Control C to exit insert mode")
                self.doc.insert(line_number)
            elif command.command == Commands.Edit:
                self.outputter("[Control C], [Enter] to exit edit mode")
                line_number = command.line_range.start if command.line_range else 1
                while line_number:
                    line_number = self.doc.edit(line_number)
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

    def save_document(self):
        """Save the document to the file"""
        save_and_overwrite(self.file_path, self.doc.lines)
        self.doc.dirty = False

    def save_macro(self):
        """Save the document to the file"""
        save_and_overwrite(Path("history.ed"), [_.original_text for _ in self.history])


def run(file_name: Optional[str] = None):
    """Set up everything except things from command line"""
    rich_printer = RichPrinter()

    def printer(text, end="\n"):
        rich_printer.print(text, end=end)

    dedlin = Dedlin(
        command_handler(), printer if file_name and file_name.endswith(".py") else print
    )
    dedlin.go(file_name)


if __name__ == "__main__":
    run()

"""
Main code.

Handles UI and links command parser to the document object
"""
from pathlib import Path
from typing import Generator, Optional

import questionary

import dedlin.help_text as help_text
from dedlin.basic_types import Command, Commands, Phrases, Printable
from dedlin.command_sources import command_generator, interactive_command_handler
from dedlin.document import Document
from dedlin.editable_input_prompt import input_with_prefill
from dedlin.file_system import read_or_create_file, save_and_overwrite
from dedlin.flash import title_screen
from dedlin.history_feature import HistoryLog
from dedlin.info_bar import display_info
from dedlin.parsers import parse_command
from dedlin.rich_output import RichPrinter
from dedlin.web import fetch_page_as_rows


def simple_input(start_line_number: int) -> Generator[str, None, None]:
    """Wrapper around questionary for insert"""
    line_number = start_line_number
    while True:
        prompt = f"   {line_number} : "
        response = questionary.text(prompt, default="").ask(kbi_msg="Exiting insert mode")
        if response is None:
            break
        yield response
        line_number += 1


class Dedlin:
    """Application for Dedlin"""

    def __init__(self, inputter: Generator[str, None, None], outputter: Printable):
        """Set up initial state and some dependency injection"""
        self.inputter = inputter
        self.command_outputter: Printable = outputter
        self.document_outputter: Printable = outputter

        self.doc: Optional[Document] = None

        self.halt_on_error = False
        """Stop on errors, useful for macros."""

        self.quit_safety = True
        """Disable checking document.dirty on quit. Useful for unit tests."""

        self.quiet = False
        """Supress most output, except from commands specifically for outputting to the screen."""

        self.vim_mode = False
        """Like quiet, except let's really try to make it unpleasant to learn and use"""

        self.echo = False
        """Write cleaned up text of command to screen"""

        self.file_path: Optional[Path] = None
        self.history: list[Command] = []
        self.history_log = HistoryLog()
        self.macro_file_name: Optional[Path] = None

    def entry_point(self, file_name: Optional[str] = None, macro_file_name: Optional[str] = None) -> int:
        """Entry point for Dedlin"""
        if self.vim_mode:
            self.quit_safety = False
            self.halt_on_error = False

        if self.vim_mode or self.quiet:
            self.echo = False
            self.command_outputter = lambda x, end="": (x, end)

        self.macro_file_name = Path(macro_file_name) if macro_file_name else None
        self.file_path = Path(file_name) if file_name else None
        lines = read_or_create_file(self.file_path)

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
                user_command_text, current_line=self.doc.current_line, document_length=len(self.doc.lines)
            )

            if command is None:
                self.command_outputter("Unknown command", end="\n")
                continue

            if not command.validate():
                self.command_outputter(f"Invalid command {command}")

            self.history.append(command)
            self.history_log.write_command_to_history_file(command.format())
            print(command.format())

            if command.command == Commands.REDO:
                command = self.history[-2]
                self.history.append(command)

            if self.echo:
                self.command_outputter(command.original_text)

            if command.command == Commands.BROWSE:
                if self.doc.dirty:
                    self.command_outputter("Discarding current document")
                if command.phrases.first is None:
                    self.command_outputter("No URL, can't browse")
                else:
                    page_as_rows = fetch_page_as_rows(command.phrases.first)
                    self.doc.lines = page_as_rows

                    self.doc.dirty = True
            elif command.command == Commands.HISTORY:
                for command in self.history:
                    self.command_outputter(command.original_text)
            elif command.command == Commands.EMPTY:
                pass
            elif command.command == Commands.LIST:
                for line, end in self.doc.list_doc(command.line_range):
                    self.document_outputter(line, end=end)
            elif command.command == Commands.PAGE:
                for line, end in self.doc.page():
                    self.document_outputter(line, end=end)
            elif command.command == Commands.SPELL:
                for line, end in self.doc.spell(command.line_range):
                    self.document_outputter(line, end=end)
            elif command.command == Commands.DELETE:
                self.doc.delete(command.line_range)
                self.command_outputter(f"Deleted lines {command.line_range.start} to {command.line_range.end}")
            elif command.command in (Commands.EXIT, Commands.QUIT):
                if command.command == Commands.QUIT and self.doc.dirty and self.quit_safety:
                    # hack!
                    self.command_outputter("Save changes? (y/n) ", end="")
                    if next(self.inputter) == "y":
                        self.save_document()
                        return 0
                elif command.command == Commands.EXIT:
                    self.save_document(command.phrases)
                if command.command in (Commands.QUIT, Commands.EXIT):
                    return 0
            elif command.command == Commands.INSERT:
                line_number = command.line_range.start if command.line_range else 1
                self.command_outputter("Control C to exit insert mode")
                self.doc.insert(line_number)
            elif command.command == Commands.PUSH:
                line_number = command.line_range.start if command.line_range else 1
                self.doc.push(line_number, command.phrases.as_list())
            elif command.command == Commands.EDIT:
                self.command_outputter("[Control C], [Enter] to exit edit mode")
                line_number = command.line_range.start if command.line_range else 1
                while line_number:
                    line_number = self.doc.edit(line_number)
            elif command.command == Commands.SEARCH:
                for text in self.doc.search(command.line_range, value=command.phrases.first):
                    self.document_outputter(text)
            elif command.command == Commands.INFO:
                for info, end in display_info(self.doc):
                    self.document_outputter(info, end)
            elif command.command == Commands.REPLACE:
                self.command_outputter("Replacing")
                for line in self.doc.replace(
                    command.line_range,
                    target=command.phrases.first,
                    replacement=command.phrases.second,
                ):
                    self.document_outputter(line, end="")
            elif command.command == Commands.LOREM:
                self.doc.lorem(command.line_range)
            elif command.command == Commands.UNDO:
                self.doc.undo()
                self.command_outputter("Undone")
            elif command.command == Commands.SORT:
                self.doc.sort()
                self.command_outputter("Sorted")
            elif command.command == Commands.REVERSE:
                self.doc.reverse()
                self.command_outputter("Reversed")
            elif command.command == Commands.SHUFFLE:
                self.doc.shuffle()
                self.command_outputter("Shuffled")
            elif command.command == Commands.CURRENT:
                self.doc.current_line = command.line_range.start
                # self.command_outputter("Current line set to {}".format(command.line_range.start))
            elif command.command == Commands.EMPTY:
                pass
            elif command.command == Commands.HELP:
                if not command.phrases or command.phrases.first is None:
                    self.command_outputter(help_text.HELP_TEXT)
                    # display | edit | files | data | reorder | meta | data | all
                elif command.phrases and command.phrases.first.upper() == "ALL":
                    for text in help_text.SPECIFIC_HELP.values():
                        self.command_outputter("")
                        self.command_outputter(text)
                elif command.phrases and command.phrases.first.upper() in help_text.SPECIFIC_HELP:
                    self.command_outputter(help_text.SPECIFIC_HELP[command.phrases.first.upper()])
                else:
                    self.command_outputter("Don't have help for that category")
            elif command.command == Commands.UNKNOWN:
                self.command_outputter("Unknown command, type HELP for help")
                if self.halt_on_error:
                    raise Exception(f"Unknown command {user_command_text}")
            else:
                self.command_outputter(f"Command {command.command} not implemented")

            if not self.quiet:
                self.command_outputter(
                    f"--- Current line is {self.doc.current_line}, {len(self.doc.lines)} lines total ---"
                )
        return 0

    def save_document(self, phrases: Optional[Phrases] = None):
        """Save the document to the file"""
        if self.file_path is not None and phrases is not None:
            self.file_path = Path(phrases.first)
        save_and_overwrite(self.file_path, self.doc.lines)
        self.doc.dirty = False

    def save_macro(self):
        """Save the document to the file"""
        save_and_overwrite(Path("history.ed"), [_.original_text for _ in self.history])


def run(
    file_name: Optional[str] = None,
    macro_file_name: Optional[str] = None,
    echo: bool = False,
    halt_on_error: bool = False,
    quit_safety: bool = False,
    vim_mode: bool = False,
) -> Dedlin:
    """Set up everything except things from command line"""
    if not macro_file_name:
        title_screen()

    rich_printer = RichPrinter()

    def printer(text, end="\n"):
        rich_printer.print(text, end="")

    if macro_file_name:
        command_handler = command_generator(Path(macro_file_name))
    else:
        command_handler = interactive_command_handler()
    dedlin = Dedlin(command_handler, printer if file_name and file_name.endswith(".py") else print)
    dedlin.halt_on_error = halt_on_error
    dedlin.echo = echo
    dedlin.quit_safety = quit_safety
    dedlin.vim_mode = vim_mode
    dedlin.entry_point(file_name, macro_file_name)
    return dedlin


if __name__ == "__main__":
    run()

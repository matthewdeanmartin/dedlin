"""
Main code.

Handles UI and links command parser to the document object
"""
from pathlib import Path
from typing import Callable, Generator, Optional

import dedlin.help_text as help_text
from dedlin.basic_types import (  # CommandGeneratorProtocol,; StringGeneratorProtocol,
    Command,
    Commands,
    Phrases,
    Printable,
    null_printer,
)
from dedlin.command_sources import InMemoryCommandGenerator
from dedlin.document import Document
from dedlin.document_sources import InMemoryInputter
from dedlin.file_system import read_or_create_file, save_and_overwrite
from dedlin.history_feature import HistoryLog
from dedlin.info_bar import display_info
from dedlin.web import fetch_page_as_rows


class Dedlin:
    """Application for Dedlin

    This class consumes clean command objects and calls the thing.

    This is a command dispatcher.
    https://en.wikipedia.org/wiki/Command_pattern
    """

    def __init__(
        self,
        inputter: InMemoryCommandGenerator,  # CommandGeneratorProtocol,
        insert_document_inputter: InMemoryInputter,  # StringGeneratorProtocol,
        edit_document_inputter: Callable[[Optional[str], str], Generator[Optional[str], None, None]],
        outputter: Callable[[Optional[str], str], None],  # Printable,
    ) -> None:
        """Set up initial state and some dependency injection"""
        self.command_inputter = inputter
        self.insert_document_inputter = insert_document_inputter
        self.edit_document_inputter = edit_document_inputter
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
            self.command_outputter = null_printer

        self.macro_file_name = Path(macro_file_name) if macro_file_name else None
        self.file_path = Path(file_name) if file_name else None
        lines = read_or_create_file(self.file_path)

        self.doc = Document(
            insert_inputter=self.insert_document_inputter,
            edit_inputter=self.edit_document_inputter,
            lines=lines,
        )
        self.command_inputter.prompt = " * "
        command_generator = self.command_inputter.generate()
        while True:
            self.command_inputter.document_length = len(self.doc.lines)
            self.command_inputter.current_line = self.doc.current_line
            try:
                command = next(command_generator)
            except KeyboardInterrupt:
                break
            except StopIteration:
                break  # it on down now

            if command is None:
                self.command_outputter("Unknown command", end="\n")
                continue

            if not command.validate():
                self.command_outputter(f"Invalid command {command}")

            self.history.append(command)
            self.history_log.write_command_to_history_file(command.format())
            if self.echo:
                self.command_outputter(command.format())

            if command.command == Commands.REDO:
                command = self.history[-2]
                self.history.append(command)

            if self.echo:
                self.command_outputter(command.original_text)

            if command.command == Commands.BROWSE:
                if self.doc.dirty:
                    self.command_outputter("Discarding current document")
                if command.phrases and command.phrases.first is None:
                    self.command_outputter("No URL, can't browse")
                elif command.phrases:
                    page_as_rows = fetch_page_as_rows(command.phrases.first)
                    self.doc.lines = page_as_rows

                    self.doc.dirty = True
            elif command.command == Commands.HISTORY:
                for command in self.history:
                    self.command_outputter(command.original_text)
            elif command.command == Commands.EMPTY:
                pass
            elif command.command == Commands.LIST and command.line_range:
                for line, end in self.doc.list_doc(command.line_range):
                    self.document_outputter(line, end=end)
            elif command.command == Commands.PAGE:
                for line, end in self.doc.page():
                    self.document_outputter(line, end=end)
            elif command.command == Commands.SPELL and command.line_range:
                for line, end in self.doc.spell(command.line_range):
                    self.document_outputter(line, end=end)
            elif command.command == Commands.DELETE and command.line_range:
                self.doc.delete(command.line_range)
                self.command_outputter(f"Deleted lines {command.line_range.start} to {command.line_range.end}")
            elif command.command in (Commands.EXIT, Commands.QUIT):
                if command.command == Commands.QUIT and self.doc.dirty and self.quit_safety:
                    # TODO: Q & E are a mess.
                    # self.command_outputter("Save changes? (y/n) ", end="")
                    # if "y" in next(generate):
                    self.save_document()
                    return 0
                elif command.command == Commands.EXIT:
                    self.save_document(command.phrases)
                if command.command in (Commands.QUIT, Commands.EXIT):
                    return 0
            elif command.command == Commands.INSERT:
                line_number = command.line_range.start if command.line_range else 1
                self.command_outputter("Control C to exit insert mode")
                self.doc.insert(line_number, command.phrases)
            elif command.command == Commands.PUSH and command.phrases and command.line_range:
                line_number = command.line_range.start if command.line_range else 1
                self.doc.push(line_number, command.phrases.as_list())
            elif command.command == Commands.EDIT:
                self.command_outputter("[Control C], [Enter] to exit edit mode")
                edit_line_number: Optional[int] = command.line_range.start if command.line_range else 1
                while edit_line_number:
                    edit_line_number = self.doc.edit(edit_line_number)
                # New line or else next text will be on the same line
                self.command_outputter("")
            elif command.command == Commands.SEARCH and command.line_range and command.phrases:
                for text in self.doc.search(command.line_range, value=command.phrases.first):
                    self.document_outputter(text)
            elif command.command == Commands.INFO:
                for info, end in display_info(self.doc):
                    self.document_outputter(info, end)
            elif command.command == Commands.REPLACE and command.phrases and command.line_range:
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
            elif command.command == Commands.CURRENT and command.line_range:
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
                    raise Exception(f"Unknown command {command.original_text}")
            else:
                self.command_outputter(f"Command {command.command} not implemented")

            if not self.quiet:
                self.command_outputter(
                    f"--- Current line is {self.doc.current_line}, {len(self.doc.lines)} lines total ---"
                )
        return 0

    def save_document(self, phrases: Optional[Phrases] = None):
        """Save the document to the file"""

        # TODO: Refactor and guarantee that the file exists when saved
        if self.doc:
            if self.file_path is not None and phrases is not None:
                self.file_path = Path(phrases.first)
            save_and_overwrite(self.file_path, self.doc.lines)
            self.doc.dirty = False

    def save_macro(self):
        """Save the document to the file"""
        save_and_overwrite(Path("history.ed"), [_.original_text for _ in self.history])

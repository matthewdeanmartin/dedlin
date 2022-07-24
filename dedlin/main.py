"""
Main code.

Handles UI and links command parser to the document object
"""
import logging
import signal
from pathlib import Path
from typing import Callable, Generator, Optional

import dedlin.help_text as help_text
from dedlin.basic_types import (  # CommandGeneratorProtocol,; StringGeneratorProtocol,
    Command,
    Commands,
    Phrases,
    Printable,
    null_printer, LineRange,
)
from dedlin.command_sources import InMemoryCommandGenerator
from dedlin.document import Document
from dedlin.document_sources import InMemoryInputter, PrefillInputter
from dedlin.file_system import read_or_create_file, save_and_overwrite
from dedlin.history_feature import HistoryLog
from dedlin.info_bar import display_info
from dedlin.web import fetch_page_as_rows

logger = logging.getLogger(__name__)


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
        edit_document_inputter: PrefillInputter,  # StringGeneratorProtocol,
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

        self.verbose = False
        """Write logging to screen, even if quiet or vim mode is enabled"""

        self.file_path: Optional[Path] = None
        self.history: list[Command] = []
        self.history_log = HistoryLog()
        self.macro_file_name: Optional[Path] = None

    def entry_point(self, file_name: Optional[str] = None, macro_file_name: Optional[str] = None) -> int:
        """Entry point for Dedlin"""
        if self.vim_mode:
            self.quit_safety = False
            self.halt_on_error = False
            # these do nothing on Windows?
            signal.signal(signal.SIGINT, lambda signum, frame: None)
            signal.signal(signal.SIGBREAK, lambda signum, frame: None)
            signal.signal(signal.SIGABRT, lambda signum, frame: None)
            print("Vim mode enabled, feedback, help and quitting disabled.")

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
                self.feedback("Unknown command")
                continue

            if not command.validate():
                self.feedback(f"Invalid command {command}")

            self.history.append(command)
            self.history_log.write_command_to_history_file(command.format())
            self.echo_if_needed(command.format())

            if command.command == Commands.REDO:
                command = self.history[-2]
                self.history.append(command)
                self.echo_if_needed(command.original_text)

            if command.command == Commands.BROWSE:
                if self.doc.dirty:
                    self.feedback("Discarding current document")
                if command.phrases and command.phrases.first is None:
                    self.feedback("No URL, can't browse")
                elif command.phrases:
                    page_as_rows = fetch_page_as_rows(command.phrases.first)
                    self.doc.lines = page_as_rows

                    self.doc.dirty = True
            elif command.command == Commands.HISTORY:
                for command in self.history:
                    # self.feedback(command.original_text.strip("\n\t\r "))
                    self.feedback(command.format())
            elif command.command == Commands.EMPTY:
                pass
            elif command.command == Commands.LIST and command.line_range:

                # TODO: move this to the Document class
                for line, end in self.doc.list_doc(command.line_range):
                    if line.endswith("\n"):
                        self.document_outputter(line, "")
                    else:
                        self.document_outputter(line, end=end)
            elif command.command == Commands.PAGE:
                # TODO: move this to the Document class
                for line, end in self.doc.page():
                    if line.endswith("\n"):
                        self.document_outputter(line, "")
                    else:
                        self.document_outputter(line, end=end)
            elif command.command == Commands.SPELL and command.line_range:
                for line, end in self.doc.spell(command.line_range):
                    self.document_outputter(line, end=end)
            elif command.command == Commands.DELETE and command.line_range:
                self.doc.delete(command.line_range)
                self.feedback(f"Deleted lines {command.line_range.start} to {command.line_range.end}")
            elif command.command in (Commands.EXIT, Commands.QUIT):
                if self.vim_mode:
                    continue
                if command.command == Commands.QUIT and self.doc.dirty and self.quit_safety:
                    # TODO: Q & E are a mess.
                    # self.command_outputter("Save changes? (y/n) ", end="")
                    # if "y" in next(generate):
                    self.save_document()
                    return 0
                if command.command == Commands.EXIT:
                    self.save_document(command.phrases)
                if command.command in (Commands.QUIT, Commands.EXIT):
                    return 0
            elif command.command == Commands.INSERT:
                line_number = command.line_range.start if command.line_range else 1
                self.feedback("Control C to exit insert mode")
                inserted = self.doc.insert(line_number, command.phrases)
                if command.phrases is None or not command.phrases.parts:
                    _ = self.history.pop()
                    rewritten_history = Command(
                        command=Commands.INSERT,
                        phrases=inserted,
                        line_range=command.line_range,
                        original_text=command.original_text,
                    )
                    self.history.append(rewritten_history)
            elif command.command == Commands.PUSH and command.phrases and command.line_range:
                line_number = command.line_range.start if command.line_range else 1
                self.doc.push(line_number, command.phrases.as_list())
            elif command.command == Commands.EDIT:
                if command.phrases and command.phrases.parts:
                    self.doc.spread(command.line_range, command.phrases.parts)
                else:
                    self.feedback("[Control C]-[Enter] to exit edit mode")
                    edit_line_number: Optional[int] = command.line_range.start if command.line_range else 1
                    can_continue = True
                    while can_continue:
                        edit_status = self.doc.edit(edit_line_number)
                        can_continue = edit_status.can_edit_again
                        if can_continue:
                            edit_line_number = edit_status.line_edited + 1

                        if edit_status.text is not None:
                            # rewrite history
                            #_ = self.history.pop()
                            self.history.append(Command(command=Commands.EDIT,
                                                        line_range=LineRange(start=edit_status.line_edited,
                                                                    offset=0),
                                                        phrases=Phrases(parts=tuple([edit_status.text]))))


                    # New line or else next text will be on the same line
                    self.command_outputter("")
            elif command.command == Commands.SEARCH and command.line_range and command.phrases:
                for text in self.doc.search(command.line_range, value=command.phrases.first):
                    self.document_outputter(text)
            elif command.command == Commands.INFO:
                for info, end in display_info(self.doc):
                    self.document_outputter(info, end)
            elif command.command == Commands.REPLACE and command.phrases and command.line_range:
                self.feedback("Replacing")
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
                self.feedback("Undone")
            elif command.command == Commands.SORT:
                self.doc.sort()
                self.feedback("Sorted")
            elif command.command == Commands.REVERSE:
                self.doc.reverse()
                self.feedback("Reversed")
            elif command.command == Commands.SHUFFLE:
                self.doc.shuffle()
                self.feedback("Shuffled")
            elif command.command == Commands.CURRENT and command.line_range:
                self.doc.current_line = command.line_range.start
            elif command.command == Commands.EMPTY:
                pass
            elif command.command == Commands.HELP:
                if not command.phrases or command.phrases.first is None:
                    self.feedback(help_text.HELP_TEXT)
                    # display | edit | files | data | reorder | meta | data | all
                elif command.phrases and command.phrases.first.upper() == "ALL":
                    for text in help_text.SPECIFIC_HELP.values():
                        self.feedback("")
                        self.feedback(text)
                elif command.phrases and command.phrases.first.upper() in help_text.SPECIFIC_HELP:
                    self.feedback(help_text.SPECIFIC_HELP[command.phrases.first.upper()])
                else:
                    self.feedback("Don't have help for that category")
            elif command.command == Commands.UNKNOWN:
                self.feedback("Unknown command, type HELP for help")
                if self.halt_on_error:
                    raise Exception(f"Unknown command {command.original_text}")
            else:
                self.feedback(f"Command {command.command} not implemented")

            self.feedback(f"--- Current line is {self.doc.current_line}, {len(self.doc.lines)} lines total ---")
        return 0

    def feedback(self, string, end="\n") -> None:
        if not (self.vim_mode or self.quiet):
            self.command_outputter(string, end)
            return

        if self.verbose:
            logger.info(string)

    def echo_if_needed(self, string, end="\n") -> None:
        """Echos a string to the outputter if needed."""
        if self.echo and not (self.vim_mode or self.quiet):
            self.command_outputter(string, end)

        if self.verbose:
            logger.info(string)

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

    def final_report(self) -> None:
        """Print out the final report"""
        self.feedback(f"History saved to {self.history_log.history_file_string}")

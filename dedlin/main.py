"""
Main code.

Handles UI and links command parser to the document object


"""

import asyncio
import logging
import os
import signal
from pathlib import Path
from types import TracebackType
from typing import Optional

from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam

import dedlin.file_system as file_system
import dedlin.text.help_text as help_text
from dedlin.ai_interface import PROLOGUE, AiClient
from dedlin.basic_types import (
    Command,
    CommandGeneratorProtocol,
    Commands,
    LineRange,
    NullPrinter,
    Phrases,
    Printable,
    StringGeneratorProtocol,
)
from dedlin.document import Document
from dedlin.history_feature import HistoryLog
from dedlin.string_comands import process_strings
from dedlin.tools.info_bar import display_info
from dedlin.tools.web import fetch_page_as_rows
from dedlin.utils.exceptions import DedlinException

logger = logging.getLogger(__name__)

HIGH_TRUST_TOOLS = [
    Commands.BROWSE,  # Web browsing
    Commands.EXPORT,  # Export to html/write file not specified in startup
    Commands.TRANSFER,  # Read arbitrary files
    Commands.MACRO,  # Read/Write arbitrary files
    Commands.CRASH,  # Halts application
    Commands.PRINT,  # Either prints to device or to new file (unimplemented)
]


class Dedlin:
    """Application for Dedlin

    This class consumes clean command objects and calls the thing.

    This is a command dispatcher.
    https://en.wikipedia.org/wiki/Command_pattern
    """

    def __init__(
        self,
        inputter: CommandGeneratorProtocol,  # OR Union[InMemoryCommandGenerator, CommandGenerator]
        insert_document_inputter: StringGeneratorProtocol,  # or Union[InMemoryInputter,....]
        edit_document_inputter: StringGeneratorProtocol,  # Union[PrefillInputter
        outputter: Printable,  # Callable[[Optional[str], str], None],  # Printable,
        headless: bool = False,
        disabled_commands: Optional[list[Commands]] = None,
        untrusted_user: bool = False,
        history: bool = True,
    ) -> None:
        """Set up initial state and some dependency injection.

        Args:
            inputter (CommandGeneratorProtocol): The inputter
            insert_document_inputter (StringGeneratorProtocol): The insert document inputter
            edit_document_inputter (StringGeneratorProtocol): The edit document inputter
            outputter (Printable): The outputter
            headless (bool): Whether to run headless. Defaults to False.
            disabled_commands (Optional[list[Commands]]): The disabled commands. Defaults to None.
            untrusted_user (bool): Whether the user is untrusted. Defaults to False.
            history (bool): Whether to save history. Defaults to True.
        """

        self.disabled_commands = disabled_commands if disabled_commands else []
        """Disable list of commands for any reason"""

        self.untrusted_user = untrusted_user
        """Disable saving to file by script argument"""

        # Autoconfigure untrusted_user mode
        if self.untrusted_user and not self.disabled_commands:
            self.disabled_commands = HIGH_TRUST_TOOLS

        self.command_inputter = inputter
        self.insert_document_inputter = insert_document_inputter
        self.edit_document_inputter = edit_document_inputter
        self.command_outputter: Printable = outputter
        self.document_outputter: Printable = outputter

        self.doc: Optional[Document] = None

        self.halt_on_error = headless  # Halt if headless.
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

        self.blind_mode = False
        """Assume user can't see at all"""

        self.enable_ai_help = False
        """Call OpenAI API to get help with commands"""

        self.headless = headless
        """No interactive features"""

        self.preferred_line_break = "\n"

        self.file_path: Optional[Path] = None
        self.history: list[Command] = []
        self.history_log = HistoryLog(persist=history)
        self.macro_file_name: Optional[Path] = None

    def entry_point(self, file_name: Optional[str] = None, macro_file_name: Optional[str] = None) -> int:
        """Entry point for Dedlin.

        Args:
            file_name (Optional[str]): The file name. Defaults to None.
            macro_file_name (Optional[str]): The macro file name. Defaults to None.

        Returns:
            int: The exit code
        """
        if self.headless and not file_name:
            raise TypeError("Headless mode requires a file name")
        if self.untrusted_user and not file_name:
            raise TypeError("Untrusted user mode requires a file name")

        if self.vim_mode and not self.headless:
            self.quit_safety = False
            self.halt_on_error = False
            # these do nothing on Windows?
            signal.signal(signal.SIGINT, lambda signum, frame: None)
            signal.signal(signal.SIGBREAK, lambda signum, frame: None)
            signal.signal(signal.SIGABRT, lambda signum, frame: None)
            print("Vim mode enabled, feedback, help and quitting disabled.")

        if self.vim_mode or self.quiet:
            self.echo = False
            self.command_outputter = NullPrinter()

        self.macro_file_name = Path(macro_file_name) if macro_file_name else None
        self.file_path = Path(file_name) if file_name else None
        if self.file_path:
            self.feedback(f"Editing {self.file_path.absolute()}")

        lines = file_system.read_or_create_file(self.file_path)

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
                self.feedback(f"Invalid command {command}")
                continue

            if command.command in self.disabled_commands:
                self.feedback(f"Command {command.command} is disabled")
                if self.headless:
                    raise DedlinException(f"Command {command.command} is disabled")
                continue

            if not command.validate():
                self.feedback(f"Invalid command {command}")
                self.print_ai_help(command)

            self.log_history(command)
            self.echo_if_needed(command.format())

            if command.command == Commands.REDO:
                try:
                    command = self.history[-2]
                except IndexError:
                    self.feedback("Nothing to redo, not enough history")
                    continue
                self.log_history(command)
                self.echo_if_needed(command.original_text or "")

            if command.command == Commands.BROWSE:
                if self.doc.dirty:
                    self.feedback("Discarding current document")
                if command.phrases and command.phrases.first is None:
                    self.feedback("No URL, can't browse")
                elif command.phrases and command.phrases.first:
                    page_as_rows = fetch_page_as_rows(command.phrases.first)
                    phrases = Phrases(parts=tuple(page_as_rows))
                    self.doc.insert(self.doc.current_line, phrases)

            elif command.command == Commands.HISTORY:
                for command in self.history:
                    # self.feedback(command.original_text.strip("\n\t\r "))
                    self.feedback(command.format(), no_comment=True)
            elif command.command == Commands.EMPTY:
                pass
            elif command.command == Commands.LIST and command.line_range:
                for line, end in self.doc.list_doc(command.line_range):
                    self.document_outputter(line, end)
            elif command.command == Commands.PAGE:
                for line, end in self.doc.page():
                    self.document_outputter(line, end)
            elif command.command == Commands.SPELL and command.line_range:
                for line, end in self.doc.spell(command.line_range):
                    self.document_outputter(line, end=end)
            elif command.command == Commands.PRINT:
                for line, end in self.doc.print(command.line_range):
                    self.document_outputter(line, end=end)
            elif command.command == Commands.DELETE and command.line_range:
                if self.doc.delete(command.line_range):
                    self.feedback(f"Deleted lines {command.line_range.start} to {command.line_range.end}")
                else:
                    self.feedback("Could not delete")
            elif command.command in (Commands.WRITE, Commands.SAVE):
                self.save_document(command.phrases)
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
                    self.log_history(rewritten_history)
                else:
                    self.log_history(command)
            elif command.command == Commands.PUSH and command.phrases and command.line_range:
                line_number = command.line_range.start if command.line_range else 1
                self.doc.push(line_number, command.phrases.as_list())
            elif command.command == Commands.COPY and command.phrases and command.line_range and command.phrases.first:
                self.doc.copy(command.line_range, int(command.phrases.first))
                self.feedback("Copied")
            elif command.command == Commands.MOVE and command.phrases and command.line_range and command.phrases.first:
                self.doc.copy(command.line_range, int(command.phrases.first))
                self.feedback("Moved")
            elif command.command == Commands.EDIT:
                if command.phrases and command.phrases.parts:
                    self.doc.spread(command.line_range, command.phrases.parts)
                else:
                    self.feedback("[Control C]-[Enter] to exit edit mode")
                    edit_line_number: int = command.line_range.start if command.line_range else 1
                    can_continue = True
                    while can_continue:
                        edit_status = self.doc.edit(edit_line_number)
                        can_continue = edit_status.can_edit_again
                        if can_continue and edit_status.line_edited:
                            edit_line_number = edit_status.line_edited + 1

                        if edit_status.text is not None and edit_status.line_edited is not None:
                            # rewrite history
                            # _ = self.history.pop()
                            self.log_history(
                                Command(
                                    command=Commands.EDIT,
                                    line_range=LineRange(start=edit_status.line_edited, offset=0),
                                    phrases=Phrases(parts=tuple([edit_status.text])),
                                )
                            )

                    # New line or else next text will be on the same line
                    self.command_outputter("")
            elif (
                command.command == Commands.SEARCH and command.line_range and command.phrases and command.phrases.first
            ):
                for text in self.doc.search(command.line_range, value=command.phrases.first):
                    self.document_outputter(text, "\n")
            elif command.command == Commands.INFO:
                for info, end in display_info(self.doc):
                    self.document_outputter(info, end)
            elif (
                command.command == Commands.REPLACE
                and command.phrases
                and command.line_range
                and command.phrases.first is not None
                and command.phrases.second is not None
            ):
                self.feedback("Replacing")
                for line in self.doc.replace(
                    command.line_range,
                    target=command.phrases.first,
                    replacement=command.phrases.second,
                ):
                    self.document_outputter(line, end="\n")
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
            elif command.command == Commands.CRASH:
                raise DedlinException("Crashing")
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
            elif command.command == Commands.EXPORT:
                file_system.export(self.file_path, self.doc.lines, self.preferred_line_break)
                self.feedback("Exported to")
            elif command.command in (
                Commands.TITLE,
                Commands.SWAPCASE,
                Commands.CASEFOLD,
                Commands.CAPITALIZE,
                Commands.UPPER,
                Commands.LOWER,
                Commands.EXPANDTABS,
                Commands.RJUST,
                Commands.LJUST,
                Commands.CENTER,
                Commands.RSTRIP,
                Commands.LSTRIP,
                Commands.STRIP,
            ):
                process_strings(self.doc.lines, command)
            elif command.command == Commands.UNKNOWN:
                self.feedback("Unknown command, type HELP for help")
                if self.halt_on_error:
                    raise DedlinException(f"Unknown command {command.original_text}")
                self.print_ai_help(command)
            else:
                self.feedback(f"Command {command.command} not implemented")

            if self.blind_mode or self.headless:
                # Concise, for screen readers, or bots
                status = f"Current line {self.doc.current_line} of {len(self.doc.lines)}"
            else:
                # Verbose, pretty for humans
                status = f"--- Current line is {self.doc.current_line}, {len(self.doc.lines)} lines total ---"
            self.feedback(status)
        return 0

    def log_history(self, command: Command) -> None:
        """Log a command to the history.

        Args:
            command (Command): The command
        """
        self.history.append(command)
        if self.history:
            self.history_log.write_command_to_history_file(command.format(), self.preferred_line_break)

    def print_ai_help(self, command: Command) -> None:
        """Print help from AI.

        Args:
            command (Command): The command
        """
        if not self.enable_ai_help:
            return
        if not os.environ.get("OPENAI_API_KEY"):
            self.feedback("No API key for AI")
            return
        client = AiClient()
        content = PROLOGUE + f" '{command.original_text}'"
        ask = ChatCompletionMessageParam(content=content, role="user")  # type: ignore
        asyncio.run(client.completion([ask]))

    def feedback(self, string: str, end: str = "\n", no_comment: bool = False) -> None:
        """Output feedback to the user.

        Args:
            string (str): The string to output
            end (str): The end string. Defaults to "\n".
            no_comment (bool): If True, don't log to history. Defaults to False.
        """
        if not no_comment:
            # prevent infinite loop for HISTORY command
            comment = Command(command=Commands.COMMENT, comment=string)
            self.log_history(command=comment)

        if not (self.vim_mode or self.quiet):
            self.command_outputter(string, end)
            return

        if self.verbose:
            logger.info(string)

    def echo_if_needed(self, string: str, end: str = "\n") -> None:
        """Echos a string to the outputter if needed.

        Args:
            string (str): The string
            end (str): The end string. Defaults to "\n".
        """
        if self.echo and not (self.vim_mode or self.quiet):
            self.command_outputter(string, end)

        if self.verbose:
            logger.info(string)

    def save_document_safe(self) -> None:
        """Save the document to the file"""
        if not self.doc:
            self.feedback("Document not initialized, can't save")
            return
        # For untrusted editors, can't save to arbitrary location
        if self.file_path is None:
            self.feedback("Can't save, no initial file name specified")
            return
        file_system.save_and_overwrite(self.file_path, self.doc.lines, self.preferred_line_break)
        self.doc.dirty = False

    def save_document(self, phrases: Optional[Phrases] = None) -> None:
        """Save the document to the file.

        Args:
            phrases (Optional[Phrases]): The phrases. Defaults to None.
        """
        if not self.doc:
            self.feedback("Document not initialized, can't save")
            return
        # TODO: Refactor and guarantee that the file exists when saved

        if self.file_path is None and phrases is not None and phrases.first and not self.untrusted_user:
            self.file_path = Path(phrases.first)
        if self.file_path is None and not self.headless and not self.untrusted_user:
            # TODO: doesn't fit with the other input/output patterns
            self.file_path = Path(input("Please specify file name: "))
        if not self.file_path and self.untrusted_user:
            self.feedback("Can't save, no initial file name specified and user is untrusted")
            return
        if not self.file_path and self.headless:
            self.feedback("Can't save in headless mode w/o initial file name.")
            return
        if not self.file_path:
            self.feedback("Need file path before saving, can't save.")
            return
        file_system.save_and_overwrite(self.file_path, self.doc.lines, self.preferred_line_break)
        self.doc.dirty = False

    def save_macro(self) -> None:
        """Save the document to the file"""

        file_system.save_and_overwrite(
            Path("history.ed"), [_.original_text for _ in self.history], self.preferred_line_break
        )

    def final_report(self) -> None:
        """Print out the final report"""
        if self.history:
            self.feedback(f"History saved to {self.history_log.history_file_string}")

    def save_on_crash(
        self, _exception_type: type[BaseException], _value: BaseException, _tb: Optional[TracebackType]
    ) -> None:
        """Save the document to the file.

        Args:
            _exception_type (type[BaseException]): The exception type
            _value (BaseException): The exception value
            _tb (Optional[TracebackType]): The traceback
        """
        self.save_document()
        # raise exception_type

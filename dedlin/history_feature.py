"""
Manage history on file system
"""
from pathlib import Path

from dedlin.utils.file_utils import locate_file


class HistoryLog:
    """Records commands in a history file"""

    @property
    def history_file_string(self) -> str:
        """String representation of the history file"""
        if self.history_file is None:
            return ""
        return str(self.history_file.resolve().absolute())

    def __init__(self, persist: bool = True) -> None:
        """Initialize the history log"""
        self.persist = persist
        if self.persist:
            self.history_file = self.initialize_history_folder() / self.make_sequential_history_file_name()
        else:
            self.history_file = None

    def initialize_history_folder(self) -> Path:
        """
        Initialize the history folder
        """
        if not self.persist:
            return Path()
        history_folder = Path(locate_file(".dedlin_history", __file__))
        if not history_folder.exists():
            history_folder.mkdir()
        return history_folder

    def count_files_in_history_folder(self) -> int:
        """
        Count the number of files in the history folder
        """
        if not self.persist:
            return 0
        history_folder = self.initialize_history_folder()
        return len(list(history_folder.glob("*.ed")))

    def make_sequential_history_file_name(self) -> str:
        """
        Make a sequential history file name
        """
        return f"history{self.count_files_in_history_folder()}.ed"

    def write_command_to_history_file(self, command: str, preferred_line_break: str) -> None:
        """
        Write a command to the history file
        """
        if not self.persist:
            return
        with open(self.history_file, "a", encoding="utf-8") as file_handle:
            file_handle.write(command)
            file_handle.write(preferred_line_break)

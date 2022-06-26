"""
Manage history on file system
"""
from pathlib import Path

from dedlin.utils.file_utils import locate_file


class HistoryLog:
    """Records commands in a history file"""
    def __init__(self) -> None:
        """ Initialize the history log """
        self.history_file = self.initialize_history_folder() / self.make_sequential_history_file_name()

    def initialize_history_folder(self):
        """
        Initialize the history folder
        """
        history_folder = Path(locate_file(".dedlin_history", __file__))
        if not history_folder.exists():
            history_folder.mkdir()
        return history_folder

    def count_files_in_history_folder(self):
        """
        Count the number of files in the history folder
        """
        history_folder = self.initialize_history_folder()
        return len(list(history_folder.glob("*.ed")))

    def make_sequential_history_file_name(self):
        """
        Make a sequential history file name
        """
        return f"history{self.count_files_in_history_folder()}.ed"

    def write_command_to_history_file(self, command: str):
        """
        Write a command to the history file
        """
        with open(self.history_file, "a", encoding="utf-8") as file_handle:
            file_handle.write(command)
            file_handle.write("\n")

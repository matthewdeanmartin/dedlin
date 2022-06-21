"""
Manage history on file system
"""
from pathlib import Path

from dedlin.utils.file_utils import locate_file


def initialize_history_folder():
    """
    Initialize the history folder
    """
    history_folder = Path(locate_file(".dedlin_history", __file__))
    if not history_folder.exists():
        history_folder.mkdir()
    return history_folder


def count_files_in_history_folder():
    """
    Count the number of files in the history folder
    """
    history_folder = initialize_history_folder()
    return len(list(history_folder.glob("*.ed")))


def make_sequential_history_file_name():
    """
    Make a sequential history file name
    """
    return f"history{count_files_in_history_folder()}.ed"


def write_command_to_history_file(command: str):
    """
    Write a command to the history file
    """
    history_file = initialize_history_folder() / make_sequential_history_file_name()
    with open(history_file, "a") as f:
        f.write(command)

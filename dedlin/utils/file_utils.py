"""
File and path manipulation
"""
import os


def locate_file(file_name: str, executing_file: str) -> str:
    """
    Find file relative to a source file, e.g.
    locate("foo/bar.txt", __file__)

    Succeeds regardless to context of execution.

    Args:
        file_name (str): The file name
        executing_file (str): The executing file

    Returns:
        str: The file path
    """
    file_path = os.path.join(os.path.dirname(os.path.abspath(executing_file)), file_name)
    return file_path

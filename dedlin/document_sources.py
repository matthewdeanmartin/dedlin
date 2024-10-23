"""
Insert and edit for documents
Allow an input prompted to be prefilled with text to be edited.

Python doesn't do this out of the box and there is a different solution
for linux than for windows.
"""

from typing import Generator, Iterable
from unittest.mock import MagicMock

import questionary

PROBABLY_WINDOWS = False
try:
    import readline

    win32console = MagicMock()
    STANDARD_IN = None
except ModuleNotFoundError:
    readline = MagicMock()
    import win32console

    PROBABLY_WINDOWS = True


# alternate windows: https://stackoverflow.com/a/11616477
if PROBABLY_WINDOWS:
    STANDARD_IN_WINDOWS = win32console.GetStdHandle(win32console.STD_INPUT_HANDLE)

    def input_with_prefill(prompt: str, default: str = "") -> str:
        """Show prompt and prefill input text with default value.

        Windows Version.

        Args:
            prompt (str): The prompt
            default (str): The default. Defaults to "".

        Returns:
            str: The input
        """
        # ref: https://stackoverflow.com/a/5888246/33264
        keys = []
        for char in default:
            evt = win32console.PyINPUT_RECORDType(win32console.KEY_EVENT)
            evt.Char = char
            evt.RepeatCount = 1
            evt.KeyDown = True
            keys.append(evt)

        STANDARD_IN_WINDOWS.WriteConsoleInput(keys)
        try:
            return input(prompt)
        except EOFError:
            return default

else:

    def input_with_prefill(prompt: str, default: str = "") -> str:
        """Show prompt and prefill input text with default value.

        Linux/Mac Version.

        Args:
            prompt (str): The prompt
            default (str): The default. Defaults to "".

        Returns:
            str: The input
        """

        # ref https://stackoverflow.com/a/8505387
        def hook() -> None:
            readline.insert_text(default)  # type: ignore
            readline.redisplay()  # type: ignore

        try:
            readline.set_pre_input_hook(hook)  # type: ignore
            result = input(prompt)
            readline.set_pre_input_hook()  # type: ignore
            return result
        except EOFError:
            return default


class SimpleInputter:
    """Get input from the user

    Implements StringGeneratorProtocol
    """

    def __init__(self) -> None:
        """Set up the inputter"""
        self.prompt: str = ""
        self.default: str = ""

    def generate(
        self,
    ) -> Generator[str, None, None]:
        """Wrapper around questionary for inserting text.

        Returns:
            Generator[str, None, None]: The input
        """
        while True:
            response = questionary.text(self.prompt, default=self.default).ask(kbi_msg="Exiting insert mode")
            if response is None:
                break
            yield response


class InMemoryInputter:
    """Get input from the user

    Implements StringGeneratorProtocol
    """

    def __init__(self, lines: Iterable[str]) -> None:
        """Set up the inputter.
        Args:
            lines (Iterable[str]): The lines
        """
        self.prompt: str = ""
        self.default: str = ""
        self.lines = lines

    def generate(
        self,
    ) -> Generator[str, None, None]:
        """Wrapper around questionary for inserting text.

        Returns:
            Generator[str, None, None]: The input
        """
        yield from self.lines


class PrefillInputter:
    """Get input from the user, used for Edit

    Implements StringGeneratorProtocol
    """

    def __init__(self) -> None:
        """Set up the inputter"""
        self.prompt: str = "* "
        self.default: str = ""

    def generate(
        self,
    ) -> Generator[str, None, None]:
        """Get input from the user.

        Returns:
            Generator[str, None, None]: The input
        """
        try:
            value = input_with_prefill(self.prompt, self.default)
            yield value
        except KeyboardInterrupt:
            yield ""

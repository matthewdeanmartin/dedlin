"""Make text editor hypothetically usable while blind."""

import logging
from typing import Optional

try:
    import pyttsx3  # type: ignore[import-not-found] # ty: ignore
except (ImportError, RuntimeError):
    pyttsx3 = None

logger = logging.getLogger(__name__)


class TalkingPrinter:
    """ "Make the output of the program more readable."""

    def __init__(self) -> None:
        """Set up initial state"""
        if pyttsx3 is not None:
            try:
                self.engine = pyttsx3.init()
            except Exception:
                self.engine = None
        else:
            self.engine = None

    # pylint:  disable=unused-argument
    def print(self, text: str, end: Optional[str], start_line: int = 0) -> None:
        """Speak.

        Args:
            text (str): The text to print
            end (Optional[str]): The end
            start_line (int): The start line. Defaults to 0.
        """
        if self.engine is None:
            logger.warning("No pyttsx3 installed, cannot speak")
            return
        if start_line > 0:
            text = f"line {start_line}: {text}"
        self.engine.say(text)
        self.engine.runAndWait()


talking_printer = TalkingPrinter()


def printer(text: Optional[str], end: str = "\n", start_line: int = 0) -> None:
    """Speak.

    Args:
        text (Optional[str]): The text to print
        end (str): The end. Defaults to "\n".
        start_line (int): The start line. Defaults to 0.
    """
    text = "" if text is None else text
    talking_printer.print(text, end=end, start_line=start_line)

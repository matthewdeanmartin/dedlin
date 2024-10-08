"""Make text editor hypothetically usable while blind."""

import logging
from typing import Optional

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

logger = logging.getLogger(__name__)


class TalkingPrinter:
    """ "Make the output of the program more readable."""

    def __init__(self) -> None:
        """Set up initial state"""
        if pyttsx3 is not None:
            self.engine = pyttsx3.init()
        else:
            self.engine = None

    # pylint:  disable=unused-argument
    def print(self, text: str, end: Optional[str]) -> None:
        """Speak.

        Args:
            text (str): The text to print
            end (Optional[str]): The end
        """
        if self.engine is None:
            logger.warning("No pyttsx3 installed, cannot speak")
            return
        self.engine.say(text)
        self.engine.runAndWait()


talking_printer = TalkingPrinter()


def printer(text: Optional[str], end: str = "\n") -> None:
    """Speak.

    Args:
        text (Optional[str]): The text to print
        end (str): The end. Defaults to "\n".
    """
    text = "" if text is None else text
    talking_printer.print(text, end=end)

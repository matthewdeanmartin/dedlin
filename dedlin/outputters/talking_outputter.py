"""Make text editor hypothetically usable while blind."""
from typing import Optional

import pyttsx3


class TalkingPrinter:
    """ "Make the output of the program more readable."""

    def __init__(self) -> None:
        """Set up initial state"""
        self.engine = pyttsx3.init()

    def print(self, text: str, end: Optional[str]) -> None:
        """Speak"""
        self.engine.say(text)
        self.engine.runAndWait()


talking_printer = TalkingPrinter()


def printer(text: Optional[str], end: str = "\n") -> None:
    text = "" if text is None else text
    talking_printer.print(text, end="")

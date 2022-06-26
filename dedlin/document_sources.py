"""
Insert and edit for documents
"""
from typing import Generator

import questionary


def simple_input(start_line_number: int) -> Generator[str, None, None]:
    """Wrapper around questionary for insert"""
    line_number = start_line_number
    while True:
        prompt = f"   {line_number} : "
        response = questionary.text(prompt, default="").ask(kbi_msg="Exiting insert mode")
        if response is None:
            break
        yield response
        line_number += 1
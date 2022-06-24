from typing import Generator


def fake_input(prompt: int) -> Generator[str, None, None]:
    yield "cat"
    yield "dog"


def fake_edit(prompt: str, initial: str) -> str:
    return "rabbit"

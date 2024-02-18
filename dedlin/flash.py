"""
Flashy stuff
"""
from art import tprint


def title_screen(user_is_blind: bool) -> None:
    """Flashy title screen.

    Args:
        user_is_blind (bool): Whether the user is blind
    """
    if not user_is_blind:
        print("\033[H\033[J", end="")
        tprint("dedlin", font="small", chr_ignore=True)

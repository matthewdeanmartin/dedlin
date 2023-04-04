"""
Flashy stuff
"""
from art import tprint


def title_screen(user_is_blind:bool) -> None:
    """Flashy title screen"""
    if not user_is_blind:
        print("\033[H\033[J", end="")
        tprint("dedlin", font="small", chr_ignore=True)

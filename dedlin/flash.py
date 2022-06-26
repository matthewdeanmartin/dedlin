"""
Flashy stuff
"""
from art import tprint


def title_screen():
    """Flashy title screen"""
    print("\033[H\033[J", end="")
    tprint("dedlin", font="small", chr_ignore=True)

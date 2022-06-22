"""
Flashy stuff
"""
from art import tprint


def title_screen():
    print("\033[H\033[J", end=""),
    tprint("dedlin", font="small", chr_ignore=True)


if __name__ == '__main__':
    title_screen()
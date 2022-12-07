#!/usr/bin/env python
# ChatGPT/Assistant wrote this
import msvcrt
import sys


def get_key():
    # Get a single keypress from the user
    return msvcrt.getch()


def clear_screen():
    # Clear the screen
    sys.stdout.write("\x1b[2J\x1b[H")


def move_cursor(row, col):
    # Move the cursor to the specified position
    sys.stdout.write(f"\x1b[{row};{col}H")


# Initialize global variables
lines = []
for _ in range(0, 20):
    lines.append(" " * 80)

current_line = 0
current_col = 0

# Main loop
while True:
    # Clear the screen and display the current lines
    clear_screen()
    for i, line in enumerate(lines):
        move_cursor(i + 1, 1)
        sys.stdout.write(line)
    move_cursor(current_line + 1, current_col + 1)

    # Get a keypress from the user
    key = get_key()

    lines[current_line] = lines[current_line][:current_col] + key.decode("utf-8") + lines[current_line][current_col:]
    current_col += 1

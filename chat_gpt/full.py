#!/usr/bin/env python

# ChatGPT/Assistant wrote this

import sys
import termios
import tty


def get_key():
    # Get a single keypress from the user
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def clear_screen():
    # Clear the screen
    print("\033[2J\033[H", end="")


def move_cursor(row, col):
    # Move the cursor to the specified position
    print(f"\033[{row};{col}H", end="")


def save_file(filename):
    # Save the file to disk
    with open(filename, "w") as f:
        for line in lines:
            f.write(line)


# Initialize global variables
lines = [[""]]
current_line = 0
current_col = 0

# Main loop
while True:
    # Clear the screen and display the current lines
    clear_screen()
    for i, line in enumerate(lines):
        move_cursor(i + 1, 1)
        print(line, end="")
    move_cursor(current_line + 1, current_col + 1)

    # Get a keypress from the user
    key = get_key()

    # Handle special keys
    if key == "\x03":
        # Control-C: quit without saving
        break
    elif key == "\x10":
        # Control-P: move cursor up
        if current_line > 0:
            current_line -= 1
            if current_col >= len(lines[current_line]):
                current_col = len(lines[current_line])
    elif key == "\x0e":
        # Control-N: move cursor down
        if current_line < len(lines) - 1:
            current_line += 1
            if current_col >= len(lines[current_line]):
                current_col = len(lines[current_line])
    elif key == "\x02":
        # Control-B: move cursor left
        if current_col > 0:
            current_col -= 1
    elif key == "\x06":
        # Control-F: move cursor right
        if current_col < len(lines[current_line]):
            current_col += 1
    elif key == "\x13":
        # Control-S: save the file and exit
        save_file("saved.txt")
        break

    # Handle regular keys
    elif key == "\n":
        # Enter: insert a newline
        lines.insert(current_line + 1, "")
        current_line += 1
        current_col = 0
    elif key == "\x08" or key == "\x7f":
        # Backspace or delete: delete a character
        if current_col == 0:
            # At the beginning of a line, merge the current line with the previous one
            if current_line > 0:
                lines[current_line - 1] += lines[current_line]
                del lines[current_line]
                current_line -= 1
                current_col = len(lines[current_line])
        else:
            # Otherwise, delete the character to the left of the cursor
            lines[current_line] = lines[current_line][: current_col - 1] + lines[current_line][current_col:]
            current_col -= 1
    else:
        # Insert the character at the current cursor position
        lines[current_line] = lines[current_line][:current_col] + key + lines[current_line][current_col:]
        current_col += 1

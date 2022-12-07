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


def save_file(filename):
    # Save the file to disk
    with open(filename, "w") as f:
        for line in lines:
            f.write(line)


# Initialize global variables
lines = []
for _ in range(0, 20):
    lines.append(" " * 80)

current_line = 0
current_col = 0

# Main loop
while True:
    # Clear the screen and display the current lines
    # clear_screen()
    # for i, line in enumerate(lines):
    #   move_cursor(i+1, 1)
    #   sys.stdout.write(line)
    # Display the current lines
    for i, line in enumerate(lines):
        move_cursor(i + 1, 1)
        sys.stdout.write(line)
    # move_cursor(current_line+1, current_col+1)

    move_cursor(current_line + 1, current_col + 1)

    # Get a keypress from the user
    key = get_key()

    # Handle special keys
    if key == b"\x03":
        # Control-C: quit without saving
        break
    elif key == b"\x00" or key == b"\xe0":
        # Escape sequence for an arrow key or function key
        key2 = get_key()
        if key2 == b"H":
            # Up arrow
            if current_line > 0:
                current_line -= 1
                if current_col >= len(lines[current_line]):
                    current_col = len(lines[current_line])
        elif key2 == b"P":
            # Down arrow
            if current_line < len(lines) - 1:
                current_line += 1
                if current_col >= len(lines[current_line]):
                    current_col = len(lines[current_line])
        elif key2 == b"K":
            # Left arrow
            if current_col > 0:
                current_col -= 1
        elif key2 == b"M":
            # Right arrow
            if current_col < len(lines[current_line]):
                current_col += 1
        elif key2 == b"S":
            # Control-S: save the file and exit
            save_file("saved.txt")
            break
        elif key == b"\x08":
            # Backspace: delete a character
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
        elif key == b"\x7f":
            # Delete: delete a character
            if current_col == len(lines[current_line]):
                # At the end of a line, merge the current line with the next one
                if current_line < len(lines) - 1:
                    lines[current_line] += lines[current_line + 1]
                    del lines[current_line + 1]
            else:
                # Otherwise, delete the character to the right of the cursor
                lines[current_line] = lines[current_line][:current_col] + lines[current_line][current_col + 1 :]
        elif key == b"\r":
            # Enter: insert a newline
            lines.insert(current_line + 1, "")
            current_line += 1
            current_col = 0
    else:
        # Insert the character at the current cursor position
        lines[current_line] = (
            lines[current_line][:current_col] + key.decode("utf-8") + lines[current_line][current_col:]
        )
        current_col += 1

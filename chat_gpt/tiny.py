#!/usr/bin/env python
# ChatGPT/Assistant wrote this
import sys


def num(line_num, line):
    # Edit a single line
    global lines
    lines[line_num] = line


def a(line):
    # Append a line below the mark
    global lines, mark
    lines.insert(mark + 1, line)
    mark += 1


def i(line_num, line):
    # Insert new lines before the mark
    global lines, mark
    lines.insert(line_num, line)
    mark = line_num


def l(start_line=0, end_line=-1):
    # List the file
    global lines
    if end_line == -1:
        end_line = len(lines)
    for i in range(start_line, end_line):
        print(f"{i}: {lines[i]}")


def d(start_line, end_line):
    # Delete lines
    global lines, mark
    if end_line == -1:
        end_line = start_line
    for i in range(end_line, start_line - 1, -1):
        del lines[i]
    mark = start_line - 1


def w(filename):
    # Write the file to disk
    with open(filename, "w") as f:
        for line in lines:
            f.write(line)


def e(filename):
    # End (write and quit)
    w(filename)
    sys.exit()


# Initialize global variables
lines = []
mark = 0

# Main loop
while True:
    try:
        # Get input from user
        user_input = input("> ")
    except EOFError:
        break

    # Split input into command and arguments
    parts = user_input.split()
    cmd = parts[0]
    args = parts[1:]

    # Execute command
    if cmd == "num":
        num(int(args[0]), args[1])
    elif cmd == "a":
        a(args[0])
    elif cmd == "i":
        i(int(args[0]), args[1])
    elif cmd == "l":
        if len(args) == 2:
            l(int(args[0]), int(args[1]))
        else:
            l()
    elif cmd == "d":
        if len(args) == 2:
            d(int(args[0]), int(args[1]))
        else:
            d(int(args[0]), -1)
    elif cmd == "w":
        w(args[0])
    elif cmd == "e":
        e(args[0])

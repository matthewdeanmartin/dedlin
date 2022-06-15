dedlin
------

This is an interactive line-by-line text editor and a DSL. Line by line text
editors suck, but they are easy to write and the DSL is mildly interesting.

## Specifications
- [help](https://www.computerhope.com/edlin.htm)
- [wikipedia](https://en.wikipedia.org/wiki/Edlin)
- [free dos](https://github.com/FDOS/edlin/blob/master/msgs-en.h)
- https://github.com/yudenisov/edlin-w32 for win10
- https://github.com/LHerrmeyer/jsedlin in js!
- https://opensource.com/article/21/6/edlin-freedos
- https://jeffpar.github.io/kbarchive/kb/067/Q67706/

## Commands
- i - Inserts lines of text.
- D - deletes the specified line, again optionally starting with the number of a line, or a range of lines. E.g.: 2,4d deletes lines 2 through 4. In the above example, line 7 was deleted.
- R - is used to replace all occurrences of a piece of text in a given range of lines, for example, to replace a spelling error. Including the ? prompts for each change. E.g.: To replace 'prit' with 'print' and to prompt for each change: ?rprit^Zprint (the ^Z represents pressing CTRL-Z). It is case-sensitive.
- S - searches for given text. It is used in the same way as replace, but without the replacement text. A search for 'apple' in the first 20 lines of a file is typed 1,20?sapple (no space, unless that is part of the search) followed by a press of enter. For each match, it asks if it is the correct one, and accepts n or y (or Enter).
- P - displays a listing of a range of lines. If no range is specified, P displays the complete file from the * to the end. This is different from L in that P changes the current line to be the last line in the range.
- T - transfers another file into the one being edited, with this syntax: \[line to insert at]t\[full path to file].
- W - (write) saves the file.
- E - saves the file and quits edlin.
- Q - quits edlin without saving.

Similar thing
https://github.com/FFengIll/vscode-edlin

tiny - https://github.com/firefish111/edlin/blob/master/main.py

dedlin
------

This is an interactive line-by-line text editor and a DSL. Line by line text
editors suck, but they are easy to write and the DSL is mildly interesting.

This is not intended to be backwards compatible with anything. Changes will be made
to make it less user hostile.

I plan to make this closer to a "mono-parse", i.e. all commands
parse to the same rigid syntax structure: `range,repeat,command,phrase,phrase`

## Implemented Commands
### Command Structure
```
([Range]) [Command] ([Phrase] ([Phrase]))
Range = Start,(End),(Repeat)
Command = [Letter]|Command
Words = "text with spaces" "text with spaces"
Words = text_without_spaces text_without_spaces
Where () means optional.
```

#### Commands
A command is either a letter or a word, e.g. I or Insert.

Commands are not case-sensitive.

Edit is the default command.

#### Ranges
A range is a 1 indexed number. In a 3 line file, the range `1,3` represents all rows

Everything up to the first letter is Range.

If the range is omitted, then either 1 or the entire document is assumed.

A single number is assumed to be a start.

Missing starts are assumed to be 1, so `,3` means `1,3`

# Concepts
A document is a series of lines.

# Features
**List, Page, Search.** These will display the document or part of it. Only Page increments the current location.
Search only displays matching rows.

**Insert and Edit.** These are the changes that require interactive input.

**Copy, Move, Delete, Sort.** These shuffle around rows.

**Join, Split.** These split or join rows based on an optional character.

**Transfer.** This inserts from disk.

**Undo.** Undoes last step.

**Quit and Exit.** These both save and exit. Exit saves without asking, Quit prompts to save if something has changed.

## Specifications/Source Inspirations
- [help](http://home.mnet-online.de/willybilly/fdhelp-dos/en/hhstndrd/base/edlin.htm)
- [help another](https://www.computerhope.com/edlin.htm)
- [wikipedia](https://en.wikipedia.org/wiki/Edlin)
- [free dos](https://github.com/FDOS/edlin/blob/master/msgs-en.h)
- [edlin-w32](https://github.com/yudenisov/edlin-w32)
- [jsedlin](https://github.com/LHerrmeyer/jsedlin)
- [edlin-freedos](https://opensource.com/article/21/6/edlin-freedos)
- [jeffpar's](https://jeffpar.github.io/kbarchive/kb/067/Q67706/)
- [vscode-edlin](https://github.com/FFengIll/vscode-edlin)
- [edlin in python](https://github.com/firefish111/edlin/blob/master/main.py)

"""Internal help text system"""

HELP_TEXT = """Command format: [start],[end],[repeat] [command] "[search]" "[replace]"
[start],[end] is abbreviated to [range]

1,10 LIST   - Lists lines 1 to 10
1 CURRENT  - Reset current line to first line
1,20 SEARCH cat - Search for cat

1  - Edit line 1
2INSERT - Insert at line 2
3INSERT "hello" - Insert "hello" at line 3
2,4DELETE - Delete lines 2 to 4
REPLACE cat dog - Replace cat with dog

For more help, type
HELP display|edit|files|data|reorder|meta|data|strings|all"""

STRINGS_HELP = """String commands
[range] TITLE - title case the range
[range] SWAPCASE = toggle current casing
[range] CASEFOLD = lowercase for foreign text
[range] CAPITALIZE = capitalize first character
[range] UPPER = Uppercase text
[range] LOWER = Lowercase text
[range] EXPANDTABS = turn tabs into spaces
[range] RJUST [width] = auto()
[range] LJUST [width] = auto()
[range] CENTER [width] - center text in span of width
[range] RSTRIP - strip trailing whitespace
[range] LSTRIP - strip leading whitespace
[range] STRIP - strip leading and trailing whitespace"""


FILES_HELP = """File System Commands
[range] Split [file name] [file name] [file name]- split file into two or three files
Quit - Exits, unless the file has been modified
Exit [file name] - Saves file and exits
"""

SPECIFIC_HELP = {
    "DISPLAY": """Display Commands
[range] List - display lines, set current to end of range
[range] Page - repeat to flip through entire document
[range] Spell - show spelling mistakes
[range] Search "[text]"
[line] Current - set current line to [line]
""",
    "EDIT": """Edit Commands
[line] - Bare number defaults to Edit at that line
[line] Insert - insert line at line number
[line] Edit - edit number
[range] Delete - delete range
[range] Replace "[text]", "[text]" - replace text in range
""",
    "DATA": """Data Source Commands
[target line] Transfer [file name] - inserts file contents to target
[range] Lorem - insert lorem ipsum text
[range] Browse [URL] - fetch web page as HTML, convert to text
""",
    "META": """Meta Commands
HISTORY [file] - list_doc all commands run
MACRO [file] - run macro
REDO - redo last command
UNDO - undo last command that changed state
HELP - display this""",
    "REORDER": """Reorder Commands
[range] Move [target line number] - move range to target
[range] Copy [target line number] - copy range to target
[range] Sort - sort lines alphabetically
[range] Shuffle - shuffle lines randomly""",
    "FILE": FILES_HELP,
    "FILES": FILES_HELP,
    "STRINGS": STRINGS_HELP,
}


if __name__ == "__main__":
    print(HELP_TEXT)
    for key, value in SPECIFIC_HELP.items():
        print(f"\n{key} commands\n")
        print(value)

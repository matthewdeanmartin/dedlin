"""Internal help text system"""

# NOT IMPLEMENTED
# [target line] Transfer [file name] - inserts file contents to target
# [range] Split [file names] - Split file

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
Save - Saves file
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
[line] - Bare number defaults to Edit at that line. Not available in headless mode.
[line] Insert - insert line at line number
[line] Edit - edit number
[range] Delete - delete range
[range] Replace "[text]", "[text]" - replace text in range
""",
    "DATA": """Data Source Commands
[range] Lorem - insert lorem ipsum text
""",
    "TOOLS": """
    [range] Browse [URL] - fetch web page as HTML, convert to text
    EXPORT - save as markdown
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

CONCISE_HELP = """
Basic Commands:
1,10 LIST - Lists lines 1-10
1 CURRENT - Reset current line to 1
1,20 SEARCH cat - Search for 'cat'
1 - Edit line 1 (not available in headless mode)
2INSERT - Interactive insert at line 2. Insert blank in headless mode.
3INSERT hello - Insert 'hello' at line 3
2,4DELETE - Delete lines 2-4
REPLACE cat dog - Replace 'cat' with 'dog'

String Commands:
[range] TITLE/SWAPCASE/CASEFOLD/CAPITALIZE/UPPER/LOWER/EXPANDTABS/RJUST [width]/LJUST [width]/CENTER [width]/RSTRIP/LSTRIP/STRIP - Various string operations

File System Commands:
Quit - Exit if no modifications
Exit [file name] - Save and exit

Command Categories
DISPLAY - List, Page, Spell, Search, Current
EDIT - Edit, Insert, Delete, Replace
DATA - Transfer, Lorem, Browse
META - HISTORY, MACRO, REDO, UNDO, HELP
REORDER - Move, Copy, Sort, Shuffle
FILES - File system commands
"""

if __name__ == "__main__":

    def run() -> None:
        """Example"""
        print(HELP_TEXT)
        for key, value in SPECIFIC_HELP.items():
            print(f"\n{key} commands\n")
            print(value)

    run()

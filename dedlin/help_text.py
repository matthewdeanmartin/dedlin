"""Internal help text system"""

HELP_TEXT = """Command format: [start],[end],[repeat] [command] "[search]" "[replace]"
[start],[end] is abbreviated to [range]

1,10 LIST   - Lists lines 1 to 10
1,20 SEARCH cat - Search for cat

1  - Edit line 1
2INSERT - Insert at line 2
2,4DELETE - Delete lines 2 to 4
REPLACE cat dog - Replace cat with dog

For more help, type
HELP display|edit|files|data|reorder|meta|data|all"""

SPECIFIC_HELP = {
    "DISPLAY": """Display Commands
[range] List - display lines, set current to end of range
[range] Page - repeat to flip through entire document
[range] Spell - show spelling mistakes
[range] Search "[text]" """,
    "EDIT": """Edit Commands
[line] - Bare number defaults to Edit at that line
[line] Insert - insert line at line number
[line] Edit - edit number
[range] Delete - delete range
[range] Replace "[text]", "[text]" - replace text in range
[range] Lorem - insert lorem ipsum text
[range] Split [file name] [file name] [file name]- split file into two or three files
""",
    "DATA": """Data Source Commands
[target line] Transfer [file name] - inserts file contents to target
[range] Browse [URL] - fetch web page as HTML, convert to text""",
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
    "FILE": """File System Commands
Quit - Exits, unless the file has been modified
Exit [file name] - Saves file and exits
""",
}

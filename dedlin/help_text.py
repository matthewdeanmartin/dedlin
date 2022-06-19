HELP_TEXT = """
Command format: [start],[end],[repeat] [command] "[search]" "[replace]"
[start],[end] is abbreviated to [range]

Display Commands
[range] List - display lines, set current to end of range
[range] Page - repeat to flip through entire document
[range] Search "[text]"

Edit Commands
[line] - Bare number defaults to Edit at that line
[line] Insert - insert line at line number
[line] Edit - edit number
[range] Delete - delete range
[target line] Transfer [file name] - inserts file contents to target
[range] Replace "[text]", "[text]" - replace text in range
[range] Lorem - insert lorem ipsum text

Meta Commands
HISTORY [file] - list all commands run
MACRO [file] - run macro
REDO - redo last command
UNDO - undo last command that changed state
HELP - display this

Reorder Commands
[range] Move [target line number] - move range to target
[range] Copy [target line number] - copy range to target
[range] Sort - sort lines alphabetically
[range] Shuffle - shuffle lines randomly

File System Commands
Quit - Exits, unless the file has been modified
Exit [file name] - Saves file and exits

"""

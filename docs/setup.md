# Setup

Dedlin starts with a file and a current line. Most commands either show lines, change lines, or move lines around.

## Start a session

```bash
dedlin notes.txt
```

At startup, Dedlin opens `notes.txt` and shows a prompt for commands.

## Basic model

- Lines are numbered from **1**
- A range such as `3,7` means lines 3 through 7
- `.` means the current line
- `$` means the last line in the document
- Commands are case-insensitive
- Quoted phrases keep spaces together

Examples:

```text
1,10 LIST
1,20 SEARCH "todo item"
REPLACE draft final
20,25 MOVE 5
```

## Saving and leaving

- `SAVE` writes the current file
- `WRITE` is accepted as a save command
- `EXIT` saves and exits
- `QUIT` exits, and if the document changed, it can ask before saving

## Output modes

- Opening a `.py` file enables richer terminal output
- `--echo` prints cleaned-up commands as they run
- `--blind_mode` favors spoken-friendly output and enables echoing

## Command history

Dedlin records command history files in `.dedlin_history`. This makes it easy to inspect or replay past editing sessions.

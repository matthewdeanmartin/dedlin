BASIC FUNCTIONALITY
- Missing parser for MOVE

ENGLISH SUPPORT
- Spell check
- Reformat for max line width
- Syntax highlighting?

TECH DEBT
- Reduce size of parser function
- Make command database for the "uniparse" object

BEHAVIOR THINGS
- Config
- Chatty Mode/Quiet Mode
  - Warnings - Not a range! etc.

COMMANDLINE THINGS
- docopts, e.g.
  - `dedlin file.txt --quiet|chatty --script=script.ed`

FILE THINGS
- Save on crash
- Implement load file, transfer
- Implement "run script"
  - Invoke from commandline
- Use more questionary things, esp for load file
  - Use questionary for confirm delete

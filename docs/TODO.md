BASIC FUNCTIONALITY
- Missing parser for MOVE and COPY
- support for "." to mean current line
- support for "$" to mean last line
- support for Append - as alias for insert to last line
- support for "Exit {file_name}" (almost! Needs tests)
- display * on List/Page for "current line"
- ? to enable/disable safety prompts
  - save
  - replace
  - delete
- Fix bug on repeated inserts/edits (I forget which)
- "Fix" to reload last command.
- Save history to ~/.dedlin_history if config says so.
- Support Config file
- SAVE MACRO to save an .ed file
- RUN MACO to run an .ed file


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

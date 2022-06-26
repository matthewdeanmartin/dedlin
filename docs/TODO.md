Current line logic
- Can't see current line, can't just change current line
- display * on List/Page for "current line"

Parser
- support for Append - as alias for insert to last line.. nope? breaks line rages
- support for "Exit {file_name}" (almost! Needs tests)

- ? to enable/disable safety prompts
  - save
  - replace
  - delete
- Fix bug on repeated inserts/edits (I forget which)
- "Fix" to reload last command.
- Save history to ~/.dedlin_history if config says so.
- Support Config file

Commands to fix/implement
- Missing parser for MOVE and COPY
- SAVE MACRO to save an .ed file
- RUN MACO to run an .ed file
- HEAD n - shortcut for 1,n LIST
- TAIL n - get bottom n lines- shortcut for $-n,$ List
- PAD n - short cut for FILL $,$+n FILL "text"
- TRIM - delete front and back if blank
- DEDUPE - keep order, remove repeating values

Shortcuts
- nFIRST - shortcut for 1,nLIST?
- nLAST - shortcut for $-n,$LIST
- nDROP - shortcut for n,$DELETE
- POP - shortcut for $,$ DELETE
- SHIFT - shortcut for 1,1 DELETE

Apply Function commands
- range UPPER - make upper case
- range EACH command, e.g. 1,2 EACH UPPER... how is this different than just range?
- line PUSH "text" --- inset via command, not interactively.

ENGLISH SUPPORT
- Spell check (1/2 done!)
- Reformat for max line width
- Sentences are lines/ Paragraphs are lines..
- Syntax highlighting? (1/100th done)

TECH DEBT
- Reduce size of parser function
- Make command database for the "uniparse" object

BEHAVIOR THINGS
- Config
- Chatty Mode/Quiet Mode
  - Warnings - Not a range! etc.
- vi/vim mode where all error messages, warnings, help messages, prompts are suppressed,
exit is disabled and control-c is disabled.

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

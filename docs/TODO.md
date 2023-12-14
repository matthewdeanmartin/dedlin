# To do

- Launch with `dedlin`, no file name, and try to save and it blows up.
- `1,50 Lorem` is broken, only outputs 1 additional line.

## AI optimizations (for bot usage)

- Restricted mode (no writing to new files!)
- No browser
- No loading snippets (Transfer)
- No saving to new file name

## Accessibility

- https://dev.to/baspin94/two-ways-to-make-your-command-line-interfaces-more-accessible-541k
- Look for various "no colors" flags to infer we are in accessible mode
- Turn off ascii art, loaders, color
- Look for tedious text re-reads/maybe support brief versions

## Process

- Try to use Githubs task tracking features to prove I can

## Current line logic

- Can't see current line, can't just change current line
- display * on List/Page for "current line"

## Parser

- support for Append - as alias for insert to last line.. nope? breaks line rages
- support for "Exit {file_name}" (almost, Needs tests)
- ? to enable/disable safety prompts
  - save
  - replace
  - delete
- Fix bug on repeated inserts/edits (I forget which)
- "Fix" to reload last command.
- Save history to ~/.dedlin_history if config says so.
- Support Config file

## Commands to fix/implement

- Missing parser for MOVE and COPY
- SAVE MACRO to save an .ed file
- RUN MACO to run an .ed file
- HEAD n - shortcut for 1,n LIST
- TAIL n - get bottom n lines- shortcut for $-n,$ List
- PAD n - short cut for FILL $,$+n FILL "text"
- TRIM - delete front and back if blank
- DEDUPE - keep order, remove repeating values

## Shortcuts

- nFIRST - shortcut for 1,nLIST?
- nLAST - shortcut for $-n,$LIST
- nDROP - shortcut for n,$DELETE
- POP - shortcut for $,$ DELETE
- SHIFT - shortcut for 1,1 DELETE

## Apply Function commands

- range UPPER - make upper case
- range EACH command, e.g. `1,2 EACH UPPER...` how is this different than just range?
- line PUSH "text" --- inset via command, not interactively.

## ENGLISH SUPPORT

- Spell check (1/2 done!)
- Reformat for max line width
- Sentences are lines/ Paragraphs are lines..
- Syntax highlighting? (1/100th done)

## TECH DEBT

- Reduce size of parser function
- Make command database for the "uniparse" object

## BEHAVIOR THINGS

- Config
- Chatty Mode/Quiet Mode
  - Warnings - Not a range! etc.

## COMMANDLINE THINGS

- docopts, e.g.
- `dedlin file.txt --quiet|chatty --script=script.ed`

## FILE THINGS

- Implement load file, transfer
- Use command inputter patter for remaining input statements

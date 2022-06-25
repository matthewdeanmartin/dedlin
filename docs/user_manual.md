# What is a line editor?
A line editor edits a list of text items. Some things are more like a list of lines 
than other things.

### Line-like
- TODO Lists
- Grocery Lists
- Most computer source code. Bash is usually a series of one-liners
- Most computer configuration files

### Somewhat line-like
- English text. Prose normally has sentences that need line breaks and paragraphs
that span many lines of text.
- Most programming languages, which like English have semantic blocks and lines
that run past the edge of the screen
- ASCII art. While creating it, you might insert rows, but once complete you 
have a block of rows that must stay together.

## Commands
Dedlin has a near-uniparse. Almost all commands can be reduced to the following form:
```
[start],[end],[repeat][Command][Word][...]
```
Where `[start],[end]` is a range of lines of text.

Where `[repeat][Command]` is a command and how many times it should be executed

Where `[Word][...]` are string positional arguments of the command.

### Command types
Commands either 

- display lines
- interactively change lines, insert, edit
- manipulate lines, e.g. delete
- reorder lines

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

# Features
**List, Page, Search.** These will display the document or part of it. Only Page increments the current location.
Search only displays matching rows.

**Insert and Edit.** These are the changes that require interactive input.

**Copy, Move, Delete, Sort.** These shuffle around rows.

**Join, Split.** These split or join rows based on an optional character.

**Transfer.** This inserts from disk.

**Undo.** Undoes last step.

**Quit and Exit.** These both save and exit. Exit saves without asking, Quit prompts to save if something has changed.

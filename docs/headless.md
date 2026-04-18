# Headless mode

Headless mode is for runs where you do not want interactive prompts.

## Best use

Headless mode works best with a file and a macro:

```bash
dedlin notes.txt --headless --macro cleanup.ed
```

That combination gives you a repeatable, non-interactive editing run.

## What changes in headless mode

- Dedlin expects a file name up front
- Status output becomes shorter and easier to parse
- A bare line number such as `7` is **not** treated as interactive edit
- Script-friendly commands are preferred over interactive insert and edit flows

For dependable automation, favor commands that include their text directly:

```text
10 EDIT Updated heading
11 INSERT New line
15,18 DELETE
SAVE
```

## Good patterns

- Keep one command per line
- Use comments to document the script
- Pair `--headless` with `--halt_on_error` when you want the run to stop on the first bad command

## Example

```text
1,15 LIST
20,22 MOVE 1
1,5 SHUFFLE
UNDO
REDO
SAVE
```

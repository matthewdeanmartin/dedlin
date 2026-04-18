# Macros

A Dedlin macro is a plain text file with one command per line.

## Run a macro

```bash
dedlin walrus.txt --macro cleanup.ed
```

For unattended runs, add headless mode:

```bash
dedlin walrus.txt --headless --macro cleanup.ed
```

## Macro file format

- One Dedlin command per line
- Blank lines are allowed
- Lines beginning with `#` are comments

Example:

```text
# Find references to Arctic
1,30 SEARCH Arctic

# Replace wording
REPLACE Arctic "Polar regions"

# Remove a section
15,18 DELETE
SAVE
```

## Good uses for macros

- recurring cleanups
- standard formatting passes
- release-note edits
- bulk text replacement across a file

## Tips

- Start by recording a small manual session and turning it into a macro
- Prefer explicit ranges over relying on the current line
- End with `SAVE` or `EXIT` if the macro should persist changes

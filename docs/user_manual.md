# Command language

Dedlin commands follow one main pattern:

```text
[range] COMMAND [arguments]
```

Examples:

```text
1,10 LIST
3 INSERT hello
8,12 DELETE
REPLACE cat dog
20,22 MOVE 1
```

## Ranges

Ranges are 1-based.

- `1` means line 1
- `1,5` means lines 1 through 5
- `,5` means lines 1 through 5
- `.` means the current line
- `$` means the last line

In interactive mode, a bare number such as `7` means **edit line 7**.

## Arguments

Arguments after the command are split on spaces unless you quote them.

```text
SEARCH walrus
REPLACE Arctic "Polar regions"
```

## Display commands

| Command | What it does |
| --- | --- |
| `LIST` | Show a range of lines |
| `PAGE` | Show the next page of lines |
| `SEARCH text` | Show matching lines |
| `SPELL` | Show spelling suggestions |
| `CURRENT` | Move the current line marker |

## Editing commands

| Command | What it does |
| --- | --- |
| `INSERT` | Insert new lines |
| `EDIT` | Replace a line interactively or inline |
| `DELETE` | Remove a range |
| `REPLACE from to` | Replace text in a range |
| `LOREM` | Insert generated placeholder text |

Examples:

```text
2 INSERT hello
10 EDIT Updated heading
15,18 DELETE
1,20 REPLACE draft final
1,50 LOREM
```

## Reordering commands

| Command | What it does |
| --- | --- |
| `COPY target` | Copy a range to another location |
| `MOVE target` | Move a range to another location |
| `SORT` | Sort the current buffer alphabetically |
| `REVERSE` | Reverse the current buffer |
| `SHUFFLE` | Shuffle the current buffer |

Examples:

```text
2,3 COPY 10
20,22 MOVE 1
SORT
REVERSE
SHUFFLE
```

## String-shaping commands

These commands act on each line in the current buffer.

| Command | What it does |
| --- | --- |
| `TITLE` | Title-case the line |
| `SWAPCASE` | Flip upper/lower case |
| `CASEFOLD` | Case-fold the line |
| `CAPITALIZE` | Capitalize the first character |
| `UPPER` | Uppercase the line |
| `LOWER` | Lowercase the line |
| `EXPANDTABS width` | Expand tabs to spaces |
| `RJUST width` | Right-justify the line |
| `LJUST width` | Left-justify the line |
| `CENTER width` | Center the line |
| `RSTRIP` | Remove trailing whitespace |
| `LSTRIP` | Remove leading whitespace |
| `STRIP` | Remove leading and trailing whitespace |

## Session and file commands

| Command | What it does |
| --- | --- |
| `SAVE` | Save the current file |
| `WRITE` | Save the current file |
| `EXIT` | Save and exit |
| `QUIT` | Exit, optionally prompting to save |
| `UNDO` | Undo the last change |
| `REDO` | Repeat the previous command from history |
| `HISTORY` | Show the command history |
| `HELP` | Show built-in help text |
| `BROWSE url` | Fetch a page and insert its text |
| `EXPORT` | Write the buffer back out using export logic |

## Comments and blank lines

Blank lines do nothing. Lines that start with `#` are treated as comments, which is especially useful in macro files.

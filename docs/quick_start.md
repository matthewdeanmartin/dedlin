# Quick start

This short session creates a small list, sorts it, and saves the file.

## 1. Open a file

```bash
dedlin groceries.txt
```

## 2. Insert a few lines

At the Dedlin prompt, type:

```text
1 INSERT
```

Then enter a few lines of text. Press `Ctrl+C` to leave insert mode.

Example:

```text
cabbage
bread
carrots
ghost peppers
coffee
tortillas
```

## 3. Show the file

```text
1,6 LIST
```

## 4. Sort the lines

```text
1,6 SORT
1,6 LIST
```

## 5. Save and exit

```text
EXIT
```

## Next steps

- Learn the command syntax in [Command language](user_manual.md)
- See [Macros](macros.md) for repeatable edits
- See [Headless mode](headless.md) for unattended runs

# Prior art

Dedlin belongs to a long line of command-driven editors.

## The lineage

Classic line editors such as **ed** and **edlin** made text editing possible on minimal terminals by focusing on lines, ranges, and short commands. Dedlin keeps that model, but aims for a friendlier day-to-day experience with more commands, better scripting support, and quality-of-life features such as syntax-aware prompts, history, and richer output modes.

## Where Dedlin fits

| Tool | Best at | How Dedlin differs |
| --- | --- | --- |
| `ed` | Minimal Unix line editing | Dedlin is less terse and adds more convenience commands |
| `edlin` | DOS-era line editing | Dedlin keeps the feel but expands the command set |
| `sed` | Stream editing in pipelines | Dedlin is interactive first, but can also run scripted edits |
| Full-screen editors | Large interactive editing sessions | Dedlin is smaller, simpler, and better suited to command-by-command changes |

## Why use a line editor today?

Line editors still shine when:

- you are working in a plain terminal
- the file is naturally line-oriented
- you want repeatable edits you can save as a macro
- you prefer explicit commands over a full-screen interface

## Historical references

- [Wikipedia: Edlin](https://en.wikipedia.org/wiki/Edlin)
- [FreeDOS EDLIN help](http://home.mnet-online.de/willybilly/fdhelp-dos/en/hhstndrd/base/edlin.htm)
- [Computer Hope EDLIN reference](https://www.computerhope.com/edlin.htm)
- [FreeDOS edlin source](https://github.com/FDOS/edlin)
- [edlin-w32](https://github.com/yudenisov/edlin-w32)
- [jsedlin](https://github.com/LHerrmeyer/jsedlin)
- [vscode-edlin](https://github.com/FFengIll/vscode-edlin)

## Related Python terminal editors

Some nearby tools take different approaches:

- [babi](https://pypi.org/project/babi/) for a full-screen terminal editor
- small curses-based editors for Linux-first workflows
- script-oriented tools where non-interactive editing matters more than an editor prompt

Dedlin sits between those worlds: it is interactive enough for manual editing, but still comfortable to script.

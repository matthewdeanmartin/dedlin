# Dedlin

Dedlin is a command-driven line editor for quick text fixes, repeatable cleanups, and batch-friendly editing. It keeps the editing model simple: load a file, target lines by number, run a command, and save.

Use this guide if you want:

- a lightweight editor over SSH or in a plain terminal
- a scriptable way to make the same edits again
- a small tool for structured text such as notes, config files, source code, or lists

## What to read first

- [Installation](installation.md) to get Dedlin onto your machine
- [Setup](setup.md) to understand the startup behavior and editing model
- [Quick start](quick_start.md) for a short hands-on session
- [Command language](user_manual.md) for the command syntax and reference

## Highlights

- Works line by line with 1-based ranges such as `1,5 LIST`
- Supports insert, edit, delete, move, copy, replace, sort, reverse, and shuffle
- Handles repeatable workflows with [macros](macros.md)
- Can run in [headless mode](headless.md) for unattended jobs
- Includes a few retro and niche features in [Easter eggs and modes](easter_eggs.md)

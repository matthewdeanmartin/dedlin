# Competition notes

This comparison is based on the command language and dispatcher that are actually wired up in the code today, mainly
`docs/user_manual.md`, `dedlin\parsers.py`, `dedlin\main.py`, and `dedlin\document.py`.

## Dedlin's implemented feature set today

Dedlin is a **line-oriented** editor, not a point-and-cursor editor. The implemented surface today is roughly:

- Display: `LIST`, `PAGE`, `SEARCH`, `SPELL`, `CURRENT`
- Editing: `INSERT`, `EDIT`, `DELETE`, `REPLACE`, `LOREM`
- Reordering: `COPY`, `MOVE`, `SORT`, `REVERSE`, `SHUFFLE`
- String shaping: case changes, tab expansion, justification, strip operations
- File/session: `SAVE`/`WRITE`, `EXIT`/`QUIT`, `HISTORY`, `HELP`, `BROWSE`, `EXPORT`
- Automation: startup macro files and headless runs

There are also some important limits in the current implementation:

- `UNDO` is only a **single previous snapshot**, not a multi-step undo history.
- `REDO` is not a true redo stack; it just replays the previous command from history.
- Some names exist in enums/help/parser but are not fully implemented end-to-end, notably `MACRO` as an in-session
  command and `TRANSFER`.
- Editing is mostly at the **whole-line** level, with text replacement as the main intra-line edit primitive.

## What `nano` has that Dedlin does not

Ignoring full-screen editing itself, `nano` still has a number of features Dedlin does not currently provide.

| Feature in nano | Status vs Dedlin |
|--------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| Character- and cursor-level editing | Missing. Dedlin tracks a current **line**, not a cursor position or column, and edits whole lines or literal substrings. |
| Go to line **and column** | Missing. Dedlin can set `CURRENT` to a line, but not a column. |
| Mark/selection, cut, and paste buffers | Missing. Dedlin has `COPY`/`MOVE` by line range, but no interactive selection, cutbuffer, or paste/yank behavior. |
| Insert another file into the current buffer | Missing in shipped behavior. `TRANSFER` appears in parser/help, but it is not dispatched in `main.py`. |
| Multiple open buffers / switching between files | Missing. Dedlin operates on one document at a time. |
| Incremental search and search-next/search-prev flow | Missing. Dedlin has literal `SEARCH`, but no interactive next/previous navigation loop. |
| Query-replace / confirm-each-replacement | Missing. `REPLACE` is unconditional over the selected range. |
| Regex search/replace | Missing. Current search/replace is plain substring based. |
| Soft wrap and paragraph justification workflow | Missing. Dedlin has line-level `LJUST`/`RJUST`/`CENTER`, but not nano-style wrapping and paragraph reflow. |
| Auto-indent and editor indentation settings | Missing as an editor behavior. There is string transformation support, but not interactive auto-indent. |
| Syntax highlighting | Missing. Rich output is only a display mode choice, not syntax-aware editing. |
| Read-only mode, backup files, autosave, lock files, recovery files | Missing. Saves overwrite the file directly. |
| Keybinding customization and rc-style configuration | Missing. Dedlin is command-language driven, not keybinding/config driven. |
| Mouse support | Missing. |
| Integrated spell correction workflow | Partially missing. Dedlin can show spelling suggestions, but not the usual interactive correct/accept flow nano users expect. |

### Bottom line vs nano

Dedlin already covers some of nano's practical basics in another form: open/save, search, replace, spelling display, and
repeatable scripted edits. What it does **not** have is most of nano's interactive editing ergonomics: cursor motion,
selection, paste buffers, wrap/justify workflow, multi-buffer work, recovery/backup behavior, and syntax-aware
presentation.

## What `emacs` has that Dedlin does not

The gap with Emacs is much larger. Even ignoring full-screen editing, Emacs is a programmable editing environment, while
Dedlin is a command-driven line editor.

| Feature in Emacs | Status vs Dedlin |
|----------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Point/mark editing model and region-based commands | Missing. Dedlin works in line ranges, not point/mark regions. |
| Character, word, sentence, paragraph, and structural navigation | Missing. Dedlin navigation is basically line-based. |
| Kill ring, yank-pop, registers, bookmarks, and rectangles | Missing. |
| Real multi-step undo/redo history | Missing. Dedlin has one-snapshot undo and command replay, not Emacs-style edit history. |
| Incremental search, regex search, query-replace, occur, isearch navigation | Missing. |
| Multiple buffers, windows, and frames | Missing. |
| Major modes and minor modes | Missing. There is no mode system comparable to Emacs editing modes. |
| Syntax highlighting, indentation engines, code navigation, completion, LSP integration | Missing. |
| Lisp extensibility and package ecosystem | Missing. Dedlin is not user-programmable in the Emacs sense. |
| Keyboard macro recording/editing/execution | Missing in the Emacs sense. Dedlin supports macro files for scripted commands, but not interactive keyboard macro recording and editing. |
| Shell, terminal, compilation, grep, project commands | Missing. |
| Dired, remote editing, version-control integration | Missing. |
| Narrowing, folding, outline features | Missing. |
| Auto-save, backup files, lock files, session restoration | Missing. |
| Rich built-in tools like Org mode, Calc, calendar, mail/news, help system depth | Missing. |

### Bottom line vs Emacs

Dedlin overlaps with Emacs only at the smallest common denominator: load text, inspect lines, replace text, reorder
content, save, and script repeatable edits. It does **not** yet offer the larger editing platform features that make
Emacs Emacs: programmable extensibility, multi-buffer workflows, structured navigation, powerful search/replace, code
intelligence, surrounding tools, or a deep editing state model.

## Summary

Compared with both `nano` and `emacs`, Dedlin's current niche is still much closer to **`ed`/`edlin` plus scripting and
convenience commands** than to a general-purpose terminal editor.

- Against `nano`, the main missing pieces are **interactive editing ergonomics**.
- Against `emacs`, the main missing pieces are **editor architecture and extensibility**.

That seems consistent with the codebase's current design: Dedlin is strongest where line ranges, explicit commands,
macros, and headless automation matter more than interactive editor UI depth.

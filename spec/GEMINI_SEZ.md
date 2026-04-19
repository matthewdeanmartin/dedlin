# Dedlin Improvement Plan (GEMINI_SEZ)

Review of the `dedlin` codebase has identified several bugs, design issues, and opportunities for enhancement.

## 1. Bugs Identified

### 1.1 `LOREM` Command Bug

- **Issue:** The `LOREM` command only appends up to the number of lines in the static `LOREM_IPSUM` list (20 lines) and always appends to the end of the document, ignoring the specified range for anything other than count calculation.
- **Confirmation:** Verified with reproduction script. `1,50 LOREM` only adds 20 lines.
- **Fix:** Update `Document.lorem` to cycle through `LOREM_IPSUM` if more lines are requested and properly handle insertion if a range is specified.

### 1.2 `SEARCH` Command Bug

- **Issue:** The `SEARCH` command displays the same line number for all matches because it uses `self.current_line` without updating it during the search loop.
- **Confirmation:** Verified with reproduction script.
- **Fix:** Calculate the correct line number for each match in `Document.search`.

### 1.3 `MOVE` Command Implementation Bug

- **Issue:** In `dedlin/main.py`, the `MOVE` command calls `self.doc.copy()` instead of `self.doc.move()`.
- **Fix:** Correct the method call in the `Dedlin.entry_point` loop.

### 1.4 `read_file` Line Ending Redundancy/Bug

- **Issue:** Manual stripping of line endings in `dedlin/file_system.py` is redundant with Python's universal newline support and potentially buggy (e.g., stripping only `\n` and leaving `\r` if they weren't already normalized).
- **Fix:** Use Python's built-in newline handling and simplify `read_file`.

### 1.5 Save Without File Name Crash

- **Issue:** Launching `dedlin` without a file name and attempting to save results in a `TypeError` because `self.file_path` remains `None`.
- **Fix:** Implement a robust check and prompt for a filename if `self.file_path` is missing before calling file system save operations.

## 2. Cross-Terminal & OS Compatibility

### 2.1 Prefill Inputter

- **Issue:** `dedlin/document_sources.py` uses platform-specific hacks for pre-filling input (`win32console` vs `readline`).
- **Recommendation:** Standardize on `questionary` or `prompt_toolkit` for all interactive inputs to ensure consistent behavior across Windows, Linux, and macOS. `prompt_toolkit` already supports pre-filled buffers.

### 2.2 Syntax Highlighting Consistency

- **Issue:** `rich_output.py` hardcodes `python` for syntax highlighting, while the interactive prompt uses a custom `EdLexer`.
- **Recommendation:** Use a more flexible approach for syntax highlighting that respects the file extension or uses a generic text highlighting when appropriate.

## 3. Usability & Features

### 3.1 Undo/Redo Depth

- **Issue:** Current implementation only supports a single level of undo.
- **Recommendation:** Implement a proper command history stack for multi-level undo/redo.

### 3.2 Parser Limitations

- **Issue:** `extract_phrases` does not handle escaped quotes.
- **Recommendation:** Update the parser to support escaped characters in quoted strings.

### 3.3 MOVE/COPY Range validation

- **Issue:** `MOVE` and `COPY` parser might be brittle for complex ranges.
- **Recommendation:** Refactor parser to use a more formal grammar or a more robust splitting logic.

## 4. Unimplemented Things (from TODO.md)

- Non-line number ranges (e.g., `/pattern/ DELETE`).
- `SAVE MACRO` and `RUN MACRO`.
- `DEDUPE`, `TRIM`, `PAD` commands.
- Config file support.

## 5. Strategy for Implementation

1. **Fix critical bugs** (`LOREM`, `SEARCH`, `MOVE` call, Save crash).
1. **Refactor input/output** for better cross-platform consistency.
1. **Enhance parser** for better range and phrase support.
1. **Implement missing core features** like Macro support and pattern-based ranges.

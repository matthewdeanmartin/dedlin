# Plan for in-session `MACRO`

## Problem

Dedlin already supports macro files at startup via `--macro`, and `parsers.py` already recognizes `MACRO` as a command. The missing piece is dispatch: once a session is running, `main.py` never handles `Commands.MACRO`, so `MACRO cleanup.ed` parses but does not execute.

That leaves Dedlin with two separate macro stories:

- **works today:** launch Dedlin with `--macro some.ed`
- **does not work today:** run `MACRO some.ed` from inside an active session

The goal is to make `MACRO` usable in-session without creating a second, inconsistent execution path.

## Recommended behavior

The recommended first version of in-session `MACRO` is:

```text
MACRO cleanup.ed
```

Behavior:

1. Load commands from the given macro file.
1. Execute them immediately against the **current document and current session state**.
1. Reuse the same validation, disabled-command checks, history logging, and feedback behavior as normal commands.
1. Resolve relative paths consistently.
1. Fail clearly on missing files, parse failures, disabled commands, or recursion limits.

Recommended scope for v1:

- Support `MACRO path.ed`
- Support nested macros only with recursion protection
- Do **not** add macro recording yet
- Do **not** add macro arguments yet
- Do **not** invent a separate macro language; keep one-command-per-line files

## Current state in code

### What already exists

- `parsers.py` recognizes `MACRO`
- `command_sources.py` has `CommandGenerator(Path)` that reads macro files and parses each line
- `docs/macros.md` documents macro files as one command per line
- `tests/test_macros.py` exercises startup macro execution in headless mode

### What is missing

- `main.py` has no `elif command.command == Commands.MACRO` branch
- Command execution is embedded inside one long loop in `entry_point`, so there is no reusable "execute this command stream" helper yet
- There is no recursion or cycle protection for macro-on-macro execution
- Path resolution rules for nested macros are not defined
- `MACRO` is currently grouped as a range-style command, even though its meaningful input is really a file path

## Proposed implementation approach

### 1. Extract command execution from the main loop

Refactor `Dedlin.entry_point()` so command fetching and command execution are separate concerns.

Recommended shape:

- `entry_point(...)` remains responsible for session setup
- add a helper like `run_command_stream(generator)` or `process_commands(generator)`
- add a helper like `execute_command(command)` for the dispatcher body

This is the key enabler. Once command execution is reusable, `MACRO` can create a file-backed generator and feed it through the same path used for interactive or startup commands.

### 2. Implement `MACRO` by reusing `CommandGenerator`

Inside the new `Commands.MACRO` branch:

- require a file path in `command.phrases.first`
- resolve it to a `Path`
- create `CommandGenerator(resolved_path)`
- run it through the shared command-stream helper

This keeps macro execution behavior aligned with startup `--macro` behavior and avoids duplicate parsing or dispatch logic.

### 3. Define path resolution rules

Recommended rule set:

- If a macro is launched from the command line with `--macro`, resolve relative paths from that macro file's directory.
- If a macro is launched in-session with `MACRO some.ed`, resolve relative paths from:
  1. the currently executing macro's directory, if already inside a macro
  1. otherwise the current process working directory

This makes nested macro references predictable.

Implementation likely needs a small macro context stack, such as:

- `self.macro_stack: list[Path]`

The top of the stack provides the base directory for nested macro resolution.

### 4. Add recursion and cycle protection

Without a guard, `a.ed` can call itself or create `a -> b -> a` loops.

Recommended protection:

- keep a stack of active macro paths
- reject execution if the target path is already on the stack
- optionally add a maximum depth cap such as 10 or 20

Suggested failure text:

- `Macro recursion detected: a.ed -> b.ed -> a.ed`

### 5. Decide control-flow semantics for `QUIT` and `EXIT` inside a macro

This needs to be explicit before implementation.

Recommended behavior:

- `SAVE` saves and continues macro execution
- `QUIT` and `EXIT` behave exactly as they do normally and terminate the session, even when invoked from a macro

Reason: this is simplest, least surprising, and matches the idea that macros are just command streams.

If that feels too strong, an alternative is to have `QUIT`/`EXIT` stop only the active macro, but that creates a second set of control-flow rules and makes behavior harder to reason about.

### 6. Tighten parser expectations for `MACRO`

Today `MACRO` is treated as a range-oriented command. That works loosely, but it is not a clean fit.

Recommended cleanup:

- move `MACRO` into the phrase-bearing command path
- make it require one phrase: the file path
- ignore line ranges for `MACRO`

This is not strictly required for a first pass, but it would make the command model less surprising and easier to maintain.

### 7. Keep security behavior consistent

`MACRO` is already listed in `HIGH_TRUST_TOOLS`. The in-session version should preserve that policy.

That means:

- disabled commands still block `MACRO`
- `untrusted_user` mode still blocks `MACRO`
- macro contents still flow through the usual disabled-command checks one command at a time

## Testing plan

### Unit tests

Add focused tests around the new dispatcher behavior:

- `MACRO file.ed` runs commands against the current document
- missing macro file reports a clear error
- nested macro executes child commands
- recursive macro call is rejected
- disabled `MACRO` is rejected
- relative path resolution works for nested macros

### Integration tests

Extend the existing macro coverage with in-session scenarios:

- start interactive/in-memory session
- run a normal edit
- run `MACRO cleanup.ed`
- verify document content and history after both

Important cases:

- macro after manual edits
- macro containing `SAVE`
- macro containing `UNDO`
- macro containing another `MACRO`
- macro containing `QUIT` or `EXIT`

## Documentation changes

Update these docs when implementing:

- `docs/macros.md`: document in-session usage
- `docs/user_manual.md`: include `MACRO file.ed` in session/file commands or meta commands
- `dedlin/text/help_text.py`: add the actual supported syntax and semantics

Example doc snippet:

```text
MACRO cleanup.ed
```

Run commands from `cleanup.ed` against the current document.

## Suggested work breakdown

1. Refactor command execution into reusable helpers.
1. Implement `Commands.MACRO` dispatch using `CommandGenerator`.
1. Add macro stack, path resolution, and recursion protection.
1. Decide and implement `QUIT`/`EXIT` behavior inside macros.
1. Add tests for in-session, nested, and recursive cases.
1. Update docs and help text.

## Risks and watchouts

- Refactoring `entry_point()` could accidentally change existing command behavior.
- History logging may become noisy or duplicated if macro wrapper commands and expanded macro commands are both logged without a clear policy.
- Nested macro path resolution can become confusing if base-directory rules are not explicit.
- `QUIT`/`EXIT` semantics inside nested macro execution can produce surprising control flow if not tested carefully.

## Recommended logging/history policy

Recommended first pass:

- log the top-level `MACRO path.ed` invocation in history
- also log the commands executed from the macro, since they really did run

That gives users an audit trail, though it may be verbose. If history becomes too noisy, a later refinement could mark macro-expanded commands as originating from a macro.

## Summary

The clean implementation path is:

- refactor command dispatch so it can execute any command generator
- reuse the existing file-backed `CommandGenerator`
- add path-resolution and recursion safety around nested macro execution
- document clear control-flow rules for macros that save or exit

That keeps in-session `MACRO` aligned with Dedlin's existing startup macro model instead of creating a separate subsystem.

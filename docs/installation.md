# Installation

Dedlin requires **Python 3.13 or newer**.

## Install as a user tool

If you already use `uv`, install Dedlin as a standalone CLI tool:

```bash
uv tool install dedlin
```

You can also use `pipx`:

```bash
pipx install dedlin
```

## Run it

Open a file in place:

```bash
dedlin notes.txt
```

If the file does not exist yet, Dedlin creates it for you.

## Docker

You can also run the published container image:

```powershell
docker run --rm -it -v "${PWD}/:/app" ghcr.io/matthewdeanmartin/dedlin:latest file.txt
```

## CLI options

```text
Usage:
  dedlin [<file>] [options]
  dedlin (-h | --help)
  dedlin --version

Options:
  -h --help          Show this screen.
  --version          Show version.
  --macro=<macro>    Run macro file.
  --echo             Echo commands.
  --halt_on_error    End program on error.
  --promptless_quit  Skip prompt on quit.
  --vim_mode         User hostile, no feedback.
  --verbose          Displaying all debugging info.
  --blind_mode       Optimize for blind users (experimental).
  --headless         Run without interactive prompts.
```

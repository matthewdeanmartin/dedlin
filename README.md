# dedlin

Dedlin is an interactive line-by-line text editor and a DSL, similar to edlin or ed. It is perfect for
letting AI chatbots edit documents without sending the whole document back and forth.

It is scriptable making it similar to `sed` for doing find, insert, replace, delete operations on existing files.

Soon it will support non-line number ranges, e.g. `"/Done/ DELETE`

Dedlin extends on [edlin](https://en.wikipedia.org/wiki/Edlin) enough that it is not backwards compatible.

I have made changes to make the app less user hostile than classic ed or edlin, but there is a `--vim_mode`
where all help, warnings, feedback will be suppressed.

## Badges

![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/dedlin)

[![Downloads](https://static.pepy.tech/personalized-badge/dedlin?period=month&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/dedlin)

[![CodeFactor](https://www.codefactor.io/repository/github/matthewdeanmartin/dedlin/badge)](https://www.codefactor.io/repository/github/matthewdeanmartin/dedlin)

## Installation

Requires python 3.11 or higher. Someday I'll write a standalone installer for it.

Install globally in an isolated virtual environment. This is a good idea.

```bash
pipx install dedlin
```

Run pre-built image with docker. Painful, but you're using an edlin clone, so that is what you're looking for.

```powershell
# This is should work in powershell or linux bash. Not windows git-bash.
docker run --rm -it -v "${PWD}/:/app"  ghcr.io/matthewdeanmartin/dedlin:latest file.txt
```

## Usage

Launch and edit file_name.txt

If you installed with `pip` or `pipx`

```bash
dedlin file_name.txt
```

Command line help

```text
> python -m dedlin --help
Dedlin.

An improved version of the edlin.

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
```

Sample session

```text
   _          _  _  _
 __| | ___  __| || |(_) _ _
/ _` |/ -_)/ _` || || || ' \
\__,_|\___|\__,_||_||_||_||_|


Editing /home/mmartin/github/dedlin/sample.txt
? * 1i
1 INSERT
Control C to exit insert mode
?    1 :  cabbage
?    2 :  bread
?    3 :  carrots
?    4 :  ghost peppers
?    5 :  coffee
?    6 :  tortillas
?    7 :

Exiting insert mode

? * SORT
 SORT
Sorted
? * LIST
1,6 LIST
   1 : bread
   2 : cabbage
   3 : carrots
   4 : coffee
   5 : ghost peppers
   6 : tortillas

? * EXIT
1,6 EXIT
```

## Documentation

- [User Manual](https://github.com/matthewdeanmartin/dedlin/blob/main/docs/user_manual.md)
- [Developer roadmap](https://github.com/matthewdeanmartin/dedlin/blob/main/docs/TODO.md)
- [Prior Art](https://github.com/matthewdeanmartin/dedlin/blob/main/docs/prior_art.md)

# dedlin

Dedlin is an interactive line-by-line text editor and a DSL. Line editors
suck, but they are easy to write and the DSL is mildly interesting.

This is not intended to be backwards compatible with anything. I have made
changes to make the app less user hostile, but there is a `--vim` mode
where all help, warnings, feedback will be suppressed.


## Installation
```bash
pip install dedlin
```

## Usage
Launch and edit file_name.txt
```bash
python -m dedlin file_name.txt
```

Command line help
```
> python -m dedlin --help
Dedlin.

An improved version of the edlin.

Usage:
  dedlin <file> [options]
  dedlin (-h | --help)
  dedlin --version

Options:
  -h --help          Show this screen.
  --version          Show version.
  --macro=<macro>    Run macro file.
  --echo             Echo commands.
  --halt_on_error    End program on error.
  --promptless_quit  Skip prompt on quit.
```

Sample session
```
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


# Documentation
- [User Manual](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/user_manual.md)
- [Developer roadmap](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/TODO.md)
- [Prior Art](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/prior_art.md)

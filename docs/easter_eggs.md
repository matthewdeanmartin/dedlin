# Easter eggs and modes

Dedlin has a few extra behaviors beyond the basic line editor workflow.

## `--vim_mode`

This is the deliberately hostile mode. Dedlin suppresses helpful feedback, disables the normal quit safety, and tries hard not to coach the user.

```bash
dedlin notes.txt --vim_mode
```

Use it if you want the old-school, unforgiving feel.

## `--blind_mode`

This experimental mode favors speech-friendly output and turns on command echoing.

```bash
dedlin notes.txt --blind_mode
```

## Splash screen

Normal interactive startup shows a retro ASCII-art title screen. It is skipped for blind mode.

## Rich output for Python files

When you open a `.py` file, Dedlin switches to a richer terminal printer instead of the plain text outputter.

## History files

Dedlin writes command history files into `.dedlin_history`, which is handy if you want to inspect how a session unfolded or reuse past commands.

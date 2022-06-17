"""
Allow an input prompted to be prefilled with text to be edited.

Python doesn't do this out of the box and there is a different solution
for linux than for windows.
"""
probably_windows = False
try:
    import readline

    _stdin = None
except ModuleNotFoundError:
    import win32console

    probably_windows = True
    _stdin = win32console.GetStdHandle(win32console.STD_INPUT_HANDLE)


# alternate windows: https://stackoverflow.com/a/11616477
if probably_windows:
    def input_with_prefill(prompt: str, default: str) -> str:
        # ref: https://stackoverflow.com/a/5888246/33264
        keys = []
        for c in default:
            evt = win32console.PyINPUT_RECORDType(win32console.KEY_EVENT)
            evt.Char = c
            evt.RepeatCount = 1
            evt.KeyDown = True
            keys.append(evt)

        _stdin.WriteConsoleInput(keys)
        return input(prompt)
else:
    def input_with_prefill(prompt: str, text: str) -> str:
        # ref https://stackoverflow.com/a/8505387
        def hook() -> None:
            readline.insert_text(text)
            readline.redisplay()

        readline.set_pre_input_hook(hook)
        result = input(prompt)
        readline.set_pre_input_hook()
        return result

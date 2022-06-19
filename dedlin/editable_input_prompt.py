"""
Allow an input prompted to be prefilled with text to be edited.

Python doesn't do this out of the box and there is a different solution
for linux than for windows.
"""
PROBABLY_WINDOWS = False
try:
    import readline

    STANDARD_IN = None
except ModuleNotFoundError:
    import win32console

    PROBABLY_WINDOWS = True
    STANDARD_IN = win32console.GetStdHandle(win32console.STD_INPUT_HANDLE)


# alternate windows: https://stackoverflow.com/a/11616477
if PROBABLY_WINDOWS:

    def input_with_prefill(prompt: str, default: str) -> str:
        """Show prompt and prefill input text with default value.

        Windows Version.
        """
        # ref: https://stackoverflow.com/a/5888246/33264
        keys = []
        for char in default:
            evt = win32console.PyINPUT_RECORDType(win32console.KEY_EVENT)
            evt.Char = char
            evt.RepeatCount = 1
            evt.KeyDown = True
            keys.append(evt)

        STANDARD_IN.WriteConsoleInput(keys)
        return input(prompt)

else:

    def input_with_prefill(prompt: str, text: str) -> str:
        """Show prompt and prefill input text with default value.

        Linux/Mac Version
        """
        # ref https://stackoverflow.com/a/8505387
        def hook() -> None:
            readline.insert_text(text)
            readline.redisplay()

        readline.set_pre_input_hook(hook)
        result = input(prompt)
        readline.set_pre_input_hook()
        return result

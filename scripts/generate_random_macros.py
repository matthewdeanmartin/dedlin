"""
This needs more business logic than I care to put into one massive decorator.
"""

import random

from dedlin.basic_types import Command, Commands, LineRange, Phrases
from dedlin.tools.lorem_data import LOREM_IPSUM


def make_range():
    start = random.randint(1, 10)
    offset = random.randint(0, 10)
    repeat = random.randint(1, 3)
    some_range = LineRange(start=start, offset=offset, repeat=repeat)
    return some_range


def some_random_words():
    words = []
    for _ in range(random.randint(1, 10)):
        lorem_line = random.choice(LOREM_IPSUM)
        lorem_word = random.choice(lorem_line.split(" "))
        words.append(lorem_word)
    return words


def two_or_more_random_words():
    words = []
    for _ in range(random.randint(2, 10)):
        lorem_line = random.choice(LOREM_IPSUM)
        lorem_word = random.choice(lorem_line.split(" "))
        words.append(lorem_word)
    return words


def make_insert():
    a_range = make_range()

    the_command = Command(
        command=Commands.INSERT,
        line_range=a_range,
        phrases=Phrases(parts=tuple(some_random_words())),
    )
    return the_command


def make_edit():
    a_range = make_range()

    the_command = Command(
        command=Commands.EDIT,
        line_range=a_range,
        phrases=Phrases(parts=tuple(some_random_words())),
    )
    return the_command


def make_copy():
    a_range = make_range()

    the_command = Command(
        command=Commands.COPY,
        line_range=a_range,
        phrases=Phrases(parts=tuple("1")),
    )
    return the_command


def make_move():
    a_range = make_range()

    the_command = Command(
        command=Commands.MOVE,
        line_range=a_range,
        phrases=Phrases(parts=tuple("1")),
    )
    return the_command


def make_push():
    a_range = make_range()

    the_command = Command(
        command=Commands.PUSH,
        line_range=a_range,
        phrases=Phrases(parts=tuple(some_random_words())),
    )
    return the_command


def make_delete():
    # should only pay attention to start-end
    a_range = make_range()

    the_command = Command(
        command=Commands.DELETE,
        line_range=a_range,
        # should be ignored.
        phrases=Phrases(parts=tuple(some_random_words())),
    )
    return the_command


def make_replace():
    a_range = make_range()

    the_command = Command(
        command=Commands.REPLACE,
        line_range=a_range,
        phrases=Phrases(parts=tuple(two_or_more_random_words())),
    )
    return the_command


def make_list():
    a_range = make_range()

    the_command = Command(
        command=Commands.LIST,
        line_range=a_range,
        phrases=Phrases(parts=tuple(two_or_more_random_words())),
    )
    return the_command


def make_page():
    a_range = make_range()

    the_command = Command(
        command=Commands.PAGE,
        line_range=a_range,
        phrases=Phrases(parts=tuple(two_or_more_random_words())),
    )
    return the_command


def make_spell():
    a_range = make_range()

    the_command = Command(
        command=Commands.SPELL,
        line_range=a_range,
        phrases=Phrases(parts=tuple(two_or_more_random_words())),
    )
    return the_command


def make_current():
    a_range = make_range()

    the_command = Command(
        command=Commands.CURRENT,
        line_range=a_range,
        phrases=Phrases(parts=tuple(two_or_more_random_words())),
    )
    return the_command


def make_search():
    a_range = make_range()

    the_command = Command(
        command=Commands.SEARCH,
        line_range=a_range,
        phrases=Phrases(parts=tuple(two_or_more_random_words())),
    )
    return the_command


def typical():
    # insert some things
    # edit some things
    macro = []
    # INSERT
    for _ in range(random.randint(1, 10)):
        macro.append(make_insert())

    # Other kinds of insert
    # BROWSE
    # LOREM

    # PUSH
    for _ in range(random.randint(1, 10)):
        macro.append(make_push())
    # EDIT
    for _ in range(random.randint(1, 10)):
        macro.append(make_edit())

    # COPY
    for _ in range(random.randint(1, 10)):
        macro.append(make_edit())

    # MOVE
    for _ in range(random.randint(1, 10)):
        macro.append(make_edit())

    # DELETE
    for _ in range(random.randint(1, 10)):
        macro.append(make_delete())

    # REPLACE
    for _ in range(random.randint(1, 10)):
        macro.append(make_replace())

    for _ in range(random.randint(1, 10)):
        macro.append(make_search())

    macro.append(Command(Commands.REVERSE))
    macro.append(Command(Commands.SHUFFLE))
    macro.append(Command(Commands.SORT))

    for index, _ in reversed(list(enumerate(macro))):
        if random.randint(0, 1):
            macro.insert(index, Command(Commands.REDO, phrases=None))
        else:
            macro.insert(index, Command(Commands.UNDO, phrases=None))

    # printing stuff
    macro.append(Command(Commands.INFO))
    macro.append(Command(Commands.HELP))
    macro.append(Command(Commands.HISTORY))

    # LIST
    for _ in range(random.randint(1, 10)):
        macro.append(make_list())
    # PAGE
    for _ in range(random.randint(1, 10)):
        macro.append(make_page())
    # SEARCH

    # SPELL
    for _ in range(random.randint(1, 10)):
        macro.append(make_spell())
    # CURRENT
    for _ in range(random.randint(1, 10)):
        macro.append(make_current())

    for line in macro:
        print(line.format())


if __name__ == "__main__":
    typical()

from collections import ChainMap

from hypothesis import given
from hypothesis import strategies as st

import dedlin.command_sources
from dedlin.basic_types import LineRange, Phrases
from dedlin.command_sources import Command


@given(
    command=st.sampled_from(dedlin.basic_types.Commands),
    line_range=st.one_of(
        st.none(),
        st.builds(LineRange, start=st.integers(1), offset=st.integers(0), repeat=st.one_of(st.just(1), st.integers(0))),
    ),
    phrases=st.one_of(
        st.none(),
        st.builds(Phrases, parts=st.tuples(st.text(), st.text())),
    ),
    original_text=st.one_of(st.none(), st.text()),
)
def test_fuzz_Command(command, line_range, phrases, original_text):
    command = dedlin.command_sources.Command(
        command=command,
        line_range=line_range,
        phrases=phrases,
        original_text=original_text,
    )
    assert command.validate()


# will just fail on bad file names
# @given(path=st.builds(Path))
# def test_fuzz_CommandGenerator(path):
#     dedlin.command_sources.CommandGenerator(path=path)


@given(
    commands=st.one_of(
        st.lists(
            st.builds(
                Command,
                line_range=st.one_of(
                    st.none(),
                    st.one_of(
                        st.none(),
                        st.builds(
                            LineRange,
                            start=st.integers(1),
                            offset=st.integers(0),
                            repeat=st.one_of(st.just(1), st.integers(0)),
                        ),
                    ),
                ),
                original_text=st.one_of(st.none(), st.one_of(st.none(), st.text())),
                phrases=st.one_of(
                    st.none(),
                    st.one_of(
                        st.none(),
                        st.builds(Phrases, parts=st.tuples(st.text(), st.text())),
                    ),
                ),
            )
        ),
        st.sets(
            st.builds(
                Command,
                line_range=st.one_of(
                    st.none(),
                    st.one_of(
                        st.none(),
                        st.builds(
                            LineRange,
                            start=st.integers(1),
                            offset=st.integers(0),
                            repeat=st.one_of(st.just(1), st.integers(0)),
                        ),
                    ),
                ),
                original_text=st.one_of(st.none(), st.one_of(st.none(), st.text())),
                phrases=st.one_of(
                    st.none(),
                    st.one_of(
                        st.none(),
                        st.builds(Phrases, parts=st.tuples(st.text(), st.text())),
                    ),
                ),
            )
        ),
        st.frozensets(
            st.builds(
                Command,
                line_range=st.one_of(
                    st.none(),
                    st.one_of(
                        st.none(),
                        st.builds(
                            LineRange,
                            start=st.integers(1),
                            offset=st.integers(0),
                            repeat=st.one_of(st.just(1), st.integers(0)),
                        ),
                    ),
                ),
                original_text=st.one_of(st.none(), st.one_of(st.none(), st.text())),
                phrases=st.one_of(
                    st.none(),
                    st.one_of(
                        st.none(),
                        st.builds(Phrases, parts=st.tuples(st.text(), st.text())),
                    ),
                ),
            )
        ),
        st.dictionaries(
            keys=st.builds(
                Command,
                line_range=st.one_of(
                    st.none(),
                    st.one_of(
                        st.none(),
                        st.builds(
                            LineRange,
                            start=st.integers(1),
                            offset=st.integers(0),
                            repeat=st.one_of(st.just(1), st.integers(0)),
                        ),
                    ),
                ),
                original_text=st.one_of(st.none(), st.one_of(st.none(), st.text())),
                phrases=st.one_of(
                    st.none(),
                    st.one_of(
                        st.none(),
                        st.builds(Phrases, parts=st.tuples(st.text(), st.text())),
                    ),
                ),
            ),
            values=st.builds(
                Command,
                line_range=st.one_of(
                    st.none(),
                    st.one_of(
                        st.none(),
                        st.builds(
                            LineRange,
                            start=st.integers(1),
                            offset=st.integers(0),
                            repeat=st.one_of(st.just(1), st.integers(0)),
                        ),
                    ),
                ),
                original_text=st.one_of(st.none(), st.one_of(st.none(), st.text())),
                phrases=st.one_of(
                    st.none(),
                    st.one_of(
                        st.none(),
                        st.builds(Phrases, parts=st.tuples(st.text(), st.text())),
                    ),
                ),
            ),
        ),
        st.dictionaries(
            keys=st.builds(
                Command,
                line_range=st.one_of(
                    st.none(),
                    st.one_of(
                        st.none(),
                        st.builds(
                            LineRange,
                            start=st.integers(1),
                            offset=st.integers(0),
                            repeat=st.one_of(st.just(1), st.integers(0)),
                        ),
                    ),
                ),
                original_text=st.one_of(st.none(), st.one_of(st.none(), st.text())),
                phrases=st.one_of(
                    st.none(),
                    st.one_of(
                        st.none(),
                        st.builds(Phrases, parts=st.tuples(st.text(), st.text())),
                    ),
                ),
            ),
            values=st.none(),
        ).map(dict.keys),
        st.dictionaries(
            keys=st.integers(),
            values=st.builds(
                Command,
                line_range=st.one_of(
                    st.none(),
                    st.one_of(
                        st.none(),
                        st.builds(
                            LineRange,
                            start=st.integers(1),
                            offset=st.integers(0),
                            repeat=st.one_of(st.just(1), st.integers(0)),
                        ),
                    ),
                ),
                original_text=st.one_of(st.none(), st.one_of(st.none(), st.text())),
                phrases=st.one_of(
                    st.none(),
                    st.one_of(
                        st.none(),
                        st.builds(Phrases, parts=st.tuples(st.text(), st.text())),
                    ),
                ),
            ),
        ).map(dict.values),
        st.iterables(
            st.builds(
                Command,
                line_range=st.one_of(
                    st.none(),
                    st.one_of(
                        st.none(),
                        st.builds(
                            LineRange,
                            start=st.integers(1),
                            offset=st.integers(0),
                            repeat=st.one_of(st.just(1), st.integers(0)),
                        ),
                    ),
                ),
                original_text=st.one_of(st.none(), st.one_of(st.none(), st.text())),
                phrases=st.one_of(
                    st.none(),
                    st.one_of(
                        st.none(),
                        st.builds(Phrases, parts=st.tuples(st.text(), st.text())),
                    ),
                ),
            )
        ),
        st.dictionaries(
            keys=st.builds(
                Command,
                line_range=st.one_of(
                    st.none(),
                    st.one_of(
                        st.none(),
                        st.builds(
                            LineRange,
                            start=st.integers(1),
                            offset=st.integers(0),
                            repeat=st.one_of(st.just(1), st.integers(0)),
                        ),
                    ),
                ),
                original_text=st.one_of(st.none(), st.one_of(st.none(), st.text())),
                phrases=st.one_of(
                    st.none(),
                    st.one_of(
                        st.none(),
                        st.builds(Phrases, parts=st.tuples(st.text(), st.text())),
                    ),
                ),
            ),
            values=st.builds(
                Command,
                line_range=st.one_of(
                    st.none(),
                    st.one_of(
                        st.none(),
                        st.builds(
                            LineRange,
                            start=st.integers(1),
                            offset=st.integers(0),
                            repeat=st.one_of(st.just(1), st.integers(min_value=0)),
                        ),
                    ),
                ),
                original_text=st.one_of(st.none(), st.one_of(st.none(), st.text())),
                phrases=st.one_of(
                    st.none(),
                    st.one_of(
                        st.none(),
                        st.builds(Phrases, parts=st.tuples(st.text(), st.text())),
                    ),
                ),
            ),
        ).map(ChainMap),
    )
)
def test_fuzz_InMemoryCommandGenerator(commands):
    generator = dedlin.command_sources.InMemoryCommandGenerator(commands=commands)
    i = 0
    for command in generator.generate():
        i += 1
        if i > 100:
            break
        # can't validate without rethinking object model
        assert command.format()


# Needs mock
# @given(prompt=st.text())
# def test_fuzz_questionary_command_handler(prompt):
#     dedlin.command_sources.questionary_command_handler(prompt=prompt)

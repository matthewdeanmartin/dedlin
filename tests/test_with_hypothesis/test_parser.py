# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

from collections import ChainMap

from hypothesis import given
from hypothesis import strategies as st

import dedlin.parsers
from dedlin.parsers import LineRange, Phrases

# TODO: replace st.nothing() with appropriate strategies


@given(
    command=st.sampled_from(dedlin.basic_types.Commands),
    line_range=st.one_of(st.none(), st.builds(LineRange, repeat=st.one_of(st.just(1), st.integers()))),
    phrases=st.one_of(
        st.none(),
        st.builds(
            Phrases,
            fifth=st.one_of(st.none(), st.one_of(st.none(), st.text())),
            fourth=st.one_of(st.none(), st.one_of(st.none(), st.text())),
            second=st.one_of(st.none(), st.one_of(st.none(), st.text())),
            third=st.one_of(st.none(), st.one_of(st.none(), st.text())),
        ),
    ),
    original_text=st.one_of(st.none(), st.text()),
)
def test_fuzz_Command(command, line_range, phrases, original_text):
    dedlin.parsers.Command(
        command=command,
        line_range=line_range,
        phrases=phrases,
        original_text=original_text,
    )


@given(start=st.integers(), end=st.integers(), repeat=st.integers())
def test_fuzz_LineRange(start, end, repeat):
    dedlin.parsers.LineRange(start=start, end=end, repeat=repeat)


@given(
    first=st.text(),
    second=st.one_of(st.none(), st.text()),
    third=st.one_of(st.none(), st.text()),
    fourth=st.one_of(st.none(), st.text()),
    fifth=st.one_of(st.none(), st.text()),
)
def test_fuzz_Phrases(first, second, third, fourth, fifth):
    dedlin.parsers.Phrases(first=first, second=second, third=third, fourth=fourth, fifth=fifth)


@given(command=st.text())
def test_fuzz_bare_command(command):
    dedlin.parsers.bare_command(command=command)


@given(
    value=st.text(),
    suffixes=st.one_of(
        st.lists(st.text()),
        st.sets(st.text()),
        st.frozensets(st.text()),
        st.dictionaries(keys=st.text(), values=st.text()),
        st.dictionaries(keys=st.text(), values=st.none()).map(dict.keys),
        st.dictionaries(keys=st.integers(), values=st.text()).map(dict.values),
        st.iterables(st.text()),
        st.dictionaries(keys=st.text(), values=st.text()).map(ChainMap),
    ),
)
def test_fuzz_ends_with_any(value, suffixes):
    dedlin.parsers.ends_with_any(value=value, suffixes=suffixes)


@given(value=st.text(), current_line=st.integers(), document_length=st.integers())
def test_fuzz_extract_one_range(value, current_line, document_length):
    dedlin.parsers.extract_one_range(value=value, current_line=current_line, document_length=document_length)


@given(value=st.text())
def test_fuzz_extract_phrases(value):
    dedlin.parsers.extract_phrases(value=value)


@given(
    value=st.text(),
    suffixes=st.one_of(
        st.lists(st.text()),
        st.sets(st.text()),
        st.frozensets(st.text()),
        st.dictionaries(keys=st.text(), values=st.text()),
        st.dictionaries(keys=st.text(), values=st.none()).map(dict.keys),
        st.dictionaries(keys=st.integers(), values=st.text()).map(dict.values),
        st.iterables(st.text()),
        st.dictionaries(keys=st.text(), values=st.text()).map(ChainMap),
    ),
)
def test_fuzz_get_command_length(value, suffixes):
    dedlin.parsers.get_command_length(value=value, suffixes=suffixes)


@given(command=st.text(), current_line=st.integers(), document_length=st.integers())
def test_fuzz_parse_command(command, current_line, document_length):
    dedlin.parsers.parse_command(command=command, current_line=current_line, document_length=document_length)


@given(
    just_command=st.text(),
    front_part=st.text(),
    original_text=st.text(),
    current_line=st.integers(),
    document_length=st.integers(),
    phrases=st.one_of(
        st.none(),
        st.builds(
            Phrases,
            fifth=st.one_of(st.none(), st.one_of(st.none(), st.text())),
            fourth=st.one_of(st.none(), st.one_of(st.none(), st.text())),
            second=st.one_of(st.none(), st.one_of(st.none(), st.text())),
            third=st.one_of(st.none(), st.one_of(st.none(), st.text())),
        ),
    ),
)
def test_fuzz_parse_range_only(just_command, front_part, original_text, current_line, document_length, phrases):
    dedlin.parsers.parse_range_only(
        just_command=just_command,
        front_part=front_part,
        original_text=original_text,
        current_line=current_line,
        document_length=document_length,
        phrases=phrases,
    )


@given(
    front_part=st.text(),
    phrases=st.one_of(
        st.none(),
        st.builds(
            Phrases,
            fifth=st.one_of(st.none(), st.one_of(st.none(), st.text())),
            fourth=st.one_of(st.none(), st.one_of(st.none(), st.text())),
            second=st.one_of(st.none(), st.one_of(st.none(), st.text())),
            third=st.one_of(st.none(), st.one_of(st.none(), st.text())),
        ),
    ),
    original_text=st.text(),
)
def test_fuzz_parse_search_replace(front_part, phrases, original_text):
    dedlin.parsers.parse_search_replace(front_part=front_part, phrases=phrases, original_text=original_text)


@given(value=st.text(), default_value=st.one_of(st.none(), st.integers()))
def test_fuzz_try_parse_int(value, default_value):
    dedlin.parsers.try_parse_int(value=value, default_value=default_value)

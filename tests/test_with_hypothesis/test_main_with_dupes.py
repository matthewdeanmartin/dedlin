# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

import typing
from pathlib import Path

import hypothesis
from hypothesis import given
from hypothesis import strategies as st

import dedlin.main
from dedlin.basic_types import Command, LineRange, StringGeneratorProtocol
from dedlin.command_sources import CommandGenerator, InteractiveGenerator
from dedlin.document_sources import SimpleInputter
from dedlin.main import Document, Phrases
from dedlin.parsers import parse_command


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
def test_fuzz_command(command, line_range, phrases, original_text):
    dedlin.main.Command(
        command=command,
        line_range=line_range,
        phrases=phrases,
        original_text=original_text,
    )


# @given(
#     inputter=st.from_type(typing.Callable[[int], typing.Generator[typing.Optional[str], None, None]]),
#     editor=st.functions(like=lambda *a, **k: None, returns=st.text()),
#     lines=st.lists(st.text()),
# )
# def test_fuzz_Document(inputter, editor, lines):
#     dedlin.main.Document(inputter=inputter, editor=editor, lines=lines)


@given(parts=st.tuples(st.text(), st.text()))
def test_fuzz_phrases(parts):
    dedlin.main.Phrases(parts=parts)


@given(macro_path=st.builds(Path))
def test_fuzz_command_generator(macro_path):
    the_generator = CommandGenerator(macro_path)
    the_generator.generate()


hypothesis.strategies.register_type_strategy(StringGeneratorProtocol, hypothesis.strategies.builds(SimpleInputter))


@given(
    document=st.builds(
        Document,
        insert_inputter=st.from_type(StringGeneratorProtocol),
        edit_inputter=st.from_type(
            typing.Callable[[typing.Optional[str], str], typing.Generator[typing.Optional[str], None, None]]
        ),
        lines=st.lists(st.text().filter(lambda s: "\n" not in s and "\r" not in s)),
    )
)
def test_fuzz_display_info(document):
    dedlin.main.display_info(document=document)


# # @given(url=st.text())
# @just("http://example.com")
# def test_fuzz_fetch_page_as_rows(url):
#     dedlin.main.fetch_page_as_rows(url=url)


# @given(prompt=st.text(), text=st.text())
# def test_fuzz_input_with_prefill(prompt, text):
#     dedlin.main.input_with_prefill(prompt=prompt, text=text)


@given(prompt=st.text())
def test_fuzz_interactive_command_handler(prompt):
    the_generator = InteractiveGenerator()
    the_generator.prompt = prompt
    the_generator.generate()


@given(
    current_command=st.builds(
        Command,
        command=st.sampled_from(dedlin.basic_types.Commands),
        line_range=st.one_of(
            st.none(),
            st.builds(
                LineRange, start=st.integers(1), offset=st.integers(0), repeat=st.one_of(st.just(1), st.integers(0))
            ),
        ),
        phrases=st.one_of(
            st.none(),
            st.builds(Phrases, parts=st.tuples(st.text(), st.text())),
        ),
        original_text=st.one_of(st.none(), st.text()),
    ),
    current_line=st.integers(0),
    document_length=st.integers(0),
)
def test_fuzz_parse_command(current_command, current_line, document_length):
    try:
        parse_command(command=current_command.format(), current_line=current_line, document_length=document_length)
    except NotImplementedError:
        pass


# @given(path=st.builds(Path))
# def test_fuzz_read_or_create_file(path):
#     dedlin.main.read_or_create_file(path=path)

#
# @given(path=st.builds(Path), lines=st.lists(st.text()))
# def test_fuzz_save_and_overwrite(path, lines):
#     dedlin.main.save_and_overwrite(path=path, lines=lines)

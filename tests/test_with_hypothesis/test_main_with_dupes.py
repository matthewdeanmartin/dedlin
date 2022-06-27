# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

import typing
from pathlib import Path

from hypothesis import example, given
from hypothesis import strategies as st

import dedlin.main
from dedlin.basic_types import LineRange, Printable
from dedlin.main import Document, Phrases


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
    dedlin.main.Command(
        command=command,
        line_range=line_range,
        phrases=phrases,
        original_text=original_text,
    )


@given(
    inputter=st.from_type(typing.Generator[str, None, None]),
    document_inputter=st.from_type(typing.Generator[str, None, None]),
    outputter=st.just(print),
)
def test_fuzz_Dedlin(inputter, document_inputter, outputter):
    dedlin.main.Dedlin(inputter=inputter, document_inputter=document_inputter, outputter=outputter)


@given(
    inputter=st.from_type(typing.Callable[[int], typing.Generator[typing.Optional[str], None, None]]),
    editor=st.functions(like=lambda *a, **k: None, returns=st.text()),
    lines=st.lists(st.text()),
)
def test_fuzz_Document(inputter, editor, lines):
    dedlin.main.Document(inputter=inputter, editor=editor, lines=lines)


@given(
    first=st.text(),
    second=st.one_of(st.none(), st.text()),
    third=st.one_of(st.none(), st.text()),
    fourth=st.one_of(st.none(), st.text()),
    fifth=st.one_of(st.none(), st.text()),
)
def test_fuzz_Phrases(first, second, third, fourth, fifth):
    dedlin.main.Phrases(first=first, second=second, third=third, fourth=fourth, fifth=fifth)


@given(macro_path=st.builds(Path))
def test_fuzz_command_generator(macro_path):
    dedlin.main.command_generator(macro_path=macro_path)


@given(document=st.builds(Document))
def test_fuzz_display_info(document):
    dedlin.main.display_info(document=document)


# @given(url=st.text())
@example("http://example.com")
def test_fuzz_fetch_page_as_rows(url):
    dedlin.main.fetch_page_as_rows(url=url)


# @given(prompt=st.text(), text=st.text())
# def test_fuzz_input_with_prefill(prompt, text):
#     dedlin.main.input_with_prefill(prompt=prompt, text=text)


@given(prompt=st.text())
def test_fuzz_interactive_command_handler(prompt):
    dedlin.main.interactive_command_handler(prompt=prompt)


@given(command=st.text(), current_line=st.integers(), document_length=st.integers())
def test_fuzz_parse_command(command, current_line, document_length):
    dedlin.main.parse_command(command=command, current_line=current_line, document_length=document_length)


# @given(path=st.builds(Path))
# def test_fuzz_read_or_create_file(path):
#     dedlin.main.read_or_create_file(path=path)

#
# @given(path=st.builds(Path), lines=st.lists(st.text()))
# def test_fuzz_save_and_overwrite(path, lines):
#     dedlin.main.save_and_overwrite(path=path, lines=lines)


@given(start_line_number=st.integers())
def test_fuzz_simple_input(start_line_number):
    dedlin.main.simple_input(start_line_number=start_line_number)

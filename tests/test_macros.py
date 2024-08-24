"""
Headless scripts do not need a companion file.
"""

from pathlib import Path

from dedlin import CommandGenerator, Dedlin
from dedlin.utils.file_utils import locate_file


def test_macros():
    for file in [
        "grep.ed",
        "sed.ed",
        "walrus_facts1.ed",
        "walrus_facts2.ed",
        "walrus_facts3.ed",
    ]:
        degenerate = Path(locate_file(f"sample_macros/{file}", __file__))
        commandGenerator = CommandGenerator(degenerate)
        results = []
        # pylint: disable=cell-var-from-loop
        app = Dedlin(
            inputter=commandGenerator,
            insert_document_inputter=None,
            edit_document_inputter=None,
            outputter=lambda x, end: results.append(x),
            headless=True,
        )

        # Read in the input file so we can copy it.
        with open(
            locate_file(f"sample_macros/{file.replace('.ed','_in.txt')}", __file__), encoding="utf-8"
        ) as input_file:
            pristine_input = input_file.read()
        output_file = f"sample_macros/{file.replace('.ed','_out.txt')}"

        # Write to a file that can be mutated
        with open(locate_file(output_file, __file__), "w", encoding="utf-8") as pristine_file:
            pristine_file.write(pristine_input)

        app.entry_point(file_name=locate_file(output_file, __file__))

        # Log results
        output_file = f"sample_macros/{file.replace('.ed', '_log.txt')}"
        with open(locate_file(output_file, __file__), "w", encoding="utf-8") as log_file:
            for line in results:
                log_file.write(line)
                log_file.write("\n")

        # TODO: add snapshot testing logic.

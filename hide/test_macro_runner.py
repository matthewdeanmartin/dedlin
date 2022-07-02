# """
# Runs a macro file as specified in the command line or `MACRO {file}` command
# """
# import logging.config
# from pathlib import Path
#
# from dedlin.__main__ import run
# from dedlin.logging_utils import configure_logging
# from dedlin.utils.file_utils import locate_file
#
# ANIMALS_FILE = Path(locate_file("sample_files/animals.txt", __file__))
#
#
# def test_lorem_ed():
#     LOGGING_CONFIG = configure_logging()
#     logging.config.dictConfig(LOGGING_CONFIG)
#
#     macro_path = Path(locate_file("sample_macros/lorem.ed", __file__))
#
#     dedlin = run(
#         file_name=str(ANIMALS_FILE.absolute()),
#         macro_file_name=str(macro_path.absolute()),
#         halt_on_error=True,
#         quit_safety=False,
#         echo=True,
#     )
#     assert dedlin.doc.lines

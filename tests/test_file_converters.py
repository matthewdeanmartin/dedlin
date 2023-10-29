from pathlib import Path
from unittest.mock import patch

import dedlin.file_converters as file_converters


def test_write_to_markdown():
    with patch.object(Path, "write_text") as patch_path:
        data_to_write = "Something"
        patch_path.return_value = data_to_write
        assert file_converters.write_to_markdown("foo.txt", ["# Title", "", "_Hello_ *world*"])

from dedlin.outputters.rich_output import RichPrinter


def test_the_rich_printer(capsys) -> None:
    printer = RichPrinter()
    printer.print("So it goes", end="\n")
    captured = capsys.readouterr()
    assert "So it goes" in captured.out

from tasks import render_report


def test_report_contents() -> None:
    assert render_report(42) == "Заявка №42\n"

from pathlib import Path

from tasks import build_report


def test_report_delivery() -> None:
    expected = Path("reports/73.txt")
    expected.unlink(missing_ok=True)
    result = build_report.delay(73)
    print(f"Задача {result.id}")
    path = Path(result.get(timeout=10))
    assert path == expected
    assert path.read_text(encoding="utf-8") == "Заявка №73\n"

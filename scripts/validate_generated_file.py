from __future__ import annotations

import json
from pathlib import Path

from unumbio_pdf_processing.validation import summarize_validation


DEFAULT_OUTPUT = Path("solution") / "output" / "BUL_EM_TM_2024000007_002.json"


def main() -> None:
    with DEFAULT_OUTPUT.open("r", encoding="utf-8") as file:
        document = json.load(file)

    records = document.get("B", {}).get("1", [])
    summary = summarize_validation(records)
    summary["output"] = str(DEFAULT_OUTPUT)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

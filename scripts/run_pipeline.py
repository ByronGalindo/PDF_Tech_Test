from __future__ import annotations

import json
from pathlib import Path

from unumbio_pdf_processing.inspection import DEFAULT_SOURCE
from unumbio_pdf_processing.pipeline import write_output_document
from unumbio_pdf_processing.validation import summarize_validation


DEFAULT_OUTPUT = Path("solution") / "output" / "BUL_EM_TM_2024000007_002.json"


def main() -> None:
    document = write_output_document(Path(DEFAULT_SOURCE), DEFAULT_OUTPUT)
    records = document.get("B", {}).get("1", [])
    validation = summarize_validation(records)

    summary = {
        "source": str(DEFAULT_SOURCE),
        "output": str(DEFAULT_OUTPUT),
        "record_count": len(records),
        "records_with_issues": validation["records_with_issues"],
        "duplicate_111_count": validation["duplicate_111_count"],
        "first_record": records[0] if records else None,
        "last_record": records[-1] if records else None,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

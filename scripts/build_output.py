from __future__ import annotations

import json
from pathlib import Path

from unumbio_pdf_processing.inspection import DEFAULT_SOURCE
from unumbio_pdf_processing.pipeline import write_output_document


DEFAULT_OUTPUT = Path("solution") / "output" / "BUL_EM_TM_2024000007_002.json"


def main() -> None:
    document = write_output_document(Path(DEFAULT_SOURCE), DEFAULT_OUTPUT)
    summary = {
        "output": str(DEFAULT_OUTPUT),
        "record_count": len(document["B"]["1"]),
        "first_record": document["B"]["1"][0] if document["B"]["1"] else None,
        "last_record": document["B"]["1"][-1] if document["B"]["1"] else None,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

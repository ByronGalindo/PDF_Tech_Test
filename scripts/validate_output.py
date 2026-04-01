from __future__ import annotations

import json
from pathlib import Path

from unumbio_pdf_processing.inspection import DEFAULT_SOURCE
from unumbio_pdf_processing.pipeline import build_output_document
from unumbio_pdf_processing.validation import summarize_validation


def main() -> None:
    document = build_output_document(Path(DEFAULT_SOURCE))
    records = document["B"]["1"]
    summary = summarize_validation(records)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

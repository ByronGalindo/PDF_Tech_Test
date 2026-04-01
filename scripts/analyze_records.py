from __future__ import annotations

import json
from pathlib import Path

from unumbio_pdf_processing.analysis import summarize_raw_records
from unumbio_pdf_processing.inspection import DEFAULT_SOURCE, load_bulletin, select_b1_pages
from unumbio_pdf_processing.records import group_raw_records
from unumbio_pdf_processing.section_detection import detect_b1_page_range


def main() -> None:
    pages = load_bulletin(Path(DEFAULT_SOURCE))
    start_page, end_page = detect_b1_page_range(pages)
    b1_pages = select_b1_pages(pages, start_page, end_page)
    records = group_raw_records(b1_pages)
    summary = summarize_raw_records(records)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path

from unumbio_pdf_processing.inspection import DEFAULT_SOURCE, load_bulletin, select_b1_pages
from unumbio_pdf_processing.records import group_raw_records, summarize_raw_record
from unumbio_pdf_processing.section_detection import detect_b1_page_range


def main() -> None:
    pages = load_bulletin(Path(DEFAULT_SOURCE))
    start_page, end_page = detect_b1_page_range(pages)
    b1_pages = select_b1_pages(pages, start_page, end_page)
    records = group_raw_records(b1_pages)

    payload = {
        "page_range": [start_page, end_page],
        "record_count": len(records),
        "first_record": summarize_raw_record(records[0]) if records else None,
        "second_record": summarize_raw_record(records[1]) if len(records) > 1 else None,
        "last_record": summarize_raw_record(records[-1]) if records else None,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

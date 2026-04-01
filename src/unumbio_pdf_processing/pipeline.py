from __future__ import annotations

import json
from pathlib import Path

from unumbio_pdf_processing.extraction import extract_records
from unumbio_pdf_processing.inspection import load_bulletin, select_b1_pages
from unumbio_pdf_processing.records import group_raw_records
from unumbio_pdf_processing.section_detection import detect_b1_page_range


def build_output_document(source_path: Path) -> dict:
    pages = load_bulletin(source_path)
    start_page, end_page = detect_b1_page_range(pages)
    b1_pages = select_b1_pages(pages, start_page, end_page)
    records = group_raw_records(b1_pages)
    extracted = extract_records(records)
    return {"B": {"1": extracted}}


def write_output_document(source_path: Path, output_path: Path) -> dict:
    document = build_output_document(source_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(document, file, indent=2, ensure_ascii=False)
        file.write("\n")
    return document

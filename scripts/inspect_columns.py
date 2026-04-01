from __future__ import annotations

import json
from pathlib import Path

from unumbio_pdf_processing.inspection import DEFAULT_SOURCE, load_bulletin, summarize_columns
from unumbio_pdf_processing.section_detection import detect_b1_page_range


def main() -> None:
    pages = load_bulletin(Path(DEFAULT_SOURCE))
    start_page, _ = detect_b1_page_range(pages)
    target_page = next(page for page in pages if page.get("page") == start_page)
    summary = summarize_columns(target_page, sample_size=12)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

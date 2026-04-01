from __future__ import annotations

from collections import Counter
from statistics import median

from unumbio_pdf_processing.records import RawRecord


def summarize_raw_records(records: list[RawRecord]) -> dict:
    if not records:
        return {
            "record_count": 0,
            "min_block_count": 0,
            "median_block_count": 0,
            "max_block_count": 0,
            "cross_page_record_count": 0,
            "cross_page_examples": [],
            "short_record_examples": [],
            "records_per_page_examples": [],
        }

    block_counts = [record.block_count for record in records]
    cross_page_records = [record for record in records if len(record.pages) > 1]
    short_records = [record for record in records if record.block_count < 10]
    page_counts = Counter(record.start_page for record in records)

    return {
        "record_count": len(records),
        "min_block_count": min(block_counts),
        "median_block_count": median(block_counts),
        "max_block_count": max(block_counts),
        "cross_page_record_count": len(cross_page_records),
        "cross_page_examples": [
            {
                "_PAGE": record.start_page,
                "pages": list(record.pages),
                "block_count": record.block_count,
                "sample": record.texts[:12],
            }
            for record in cross_page_records[:5]
        ],
        "short_record_examples": [
            {
                "_PAGE": record.start_page,
                "pages": list(record.pages),
                "block_count": record.block_count,
                "sample": record.texts[:12],
            }
            for record in short_records[:5]
        ],
        "records_per_page_examples": [
            {"page": page, "count": count}
            for page, count in sorted(page_counts.items())[:10]
        ],
    }

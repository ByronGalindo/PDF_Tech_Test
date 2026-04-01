from __future__ import annotations

import json
from pathlib import Path
from statistics import median

from unumbio_pdf_processing.section_detection import detect_b1_page_range


DEFAULT_SOURCE = Path("UNUMBIO PDF PROCESSING") / "BUL_EM_TM_2024000007_001.json"


def load_bulletin(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def select_b1_pages(
    pages: list[dict],
    start_page: int,
    end_page: int,
) -> list[dict]:
    return [page for page in pages if start_page <= page.get("page", -1) <= end_page]


def summarize_page(page: dict) -> dict:
    textboxes = page.get("textboxhorizontal", [])
    x0_values = sorted(
        box["x0"]
        for box in textboxes
        if isinstance(box, dict) and isinstance(box.get("x0"), (int, float))
    )
    return {
        "page": page.get("page"),
        "textboxes": len(textboxes),
        "min_x0": round(x0_values[0], 3) if x0_values else None,
        "median_x0": round(median(x0_values), 3) if x0_values else None,
        "max_x0": round(x0_values[-1], 3) if x0_values else None,
        "sample_text": [
            clean_text(box.get("text", ""))
            for box in textboxes[:8]
            if isinstance(box, dict) and box.get("text")
        ],
    }


def clean_text(value: str) -> str:
    return " ".join(value.split())


def summarize_b1_range(path: Path = DEFAULT_SOURCE) -> dict:
    pages = load_bulletin(path)
    start_page, end_page = detect_b1_page_range(pages)
    selected_pages = select_b1_pages(pages, start_page, end_page)
    return {
        "source": str(path),
        "page_range": [start_page, end_page],
        "pages_found": len(selected_pages),
        "first_page": summarize_page(selected_pages[0]) if selected_pages else None,
        "last_page": summarize_page(selected_pages[-1]) if selected_pages else None,
    }

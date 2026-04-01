from __future__ import annotations

"""Helpers to detect where section B.1 starts and ends."""


def normalize_text(value: str) -> str:
    """Normalize extracted PDF text for heading comparisons."""
    return " ".join(value.split()).strip().lower()


def collect_page_texts(page: dict) -> list[str]:
    """Collect normalized text fragments from one page."""
    texts: list[str] = []
    for box in page.get("textboxhorizontal", []):
        if not isinstance(box, dict):
            continue
        text = box.get("text")
        if not text:
            continue
        normalized = normalize_text(text)
        if normalized:
            texts.append(normalized)
    return texts


def page_contains_any(page: dict, candidates: set[str]) -> bool:
    """Check whether a page contains any of the requested markers."""
    page_texts = collect_page_texts(page)
    return any(text in candidates for text in page_texts)


def detect_b1_page_range(pages: list[dict]) -> tuple[int, int]:
    """Detect the inclusive page range that belongs to section B.1."""
    b1_markers = {"b.1.", "b.1", "part b.1.", "part b.1"}
    b2_markers = {"b.2.", "b.2", "part b.2.", "part b.2"}

    start_page: int | None = None
    end_page: int | None = None

    for page in pages:
        page_number = page.get("page")
        if not isinstance(page_number, int):
            continue

        if start_page is None and page_contains_any(page, b1_markers):
            start_page = page_number
            continue

        if start_page is not None and page_contains_any(page, b2_markers):
            end_page = page_number - 1
            break

    if start_page is None:
        raise ValueError("Could not detect the start of section B.1.")

    if end_page is None:
        end_page = max(
            page.get("page") for page in pages if isinstance(page.get("page"), int)
        )

    return start_page, end_page

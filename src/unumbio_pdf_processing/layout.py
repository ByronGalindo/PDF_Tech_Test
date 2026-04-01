from __future__ import annotations

from dataclasses import dataclass


INID_MARKERS = {
    "111",
    "151",
    "180",
    "210",
    "220",
    "300",
    "400",
    "441",
    "442",
    "450",
    "521",
    "531",
    "540",
    "546",
    "554",
}


@dataclass(frozen=True)
class TextBlock:
    page: int
    text: str
    x0: float
    x1: float
    top: float
    bottom: float

    @property
    def center_x(self) -> float:
        return (self.x0 + self.x1) / 2


def clean_text(value: str) -> str:
    return " ".join(value.split()).strip()


def extract_text_blocks(page: dict) -> list[TextBlock]:
    page_number = page.get("page")
    if not isinstance(page_number, int):
        return []

    blocks: list[TextBlock] = []
    for item in page.get("textboxhorizontal", []):
        if not isinstance(item, dict):
            continue

        text = clean_text(item.get("text", ""))
        x0 = item.get("x0")
        x1 = item.get("x1")
        top = item.get("top")
        bottom = item.get("bottom")

        if not text:
            continue
        if not all(isinstance(value, (int, float)) for value in (x0, x1, top, bottom)):
            continue

        blocks.append(
            TextBlock(
                page=page_number,
                text=text,
                x0=float(x0),
                x1=float(x1),
                top=float(top),
                bottom=float(bottom),
            )
        )

    return blocks


def detect_content_top(blocks: list[TextBlock]) -> float:
    marker_tops = [block.top for block in blocks if block.text in INID_MARKERS]
    if not marker_tops:
        return 0.0
    return min(marker_tops)


def content_text_blocks(page: dict) -> list[TextBlock]:
    blocks = extract_text_blocks(page)
    content_top = detect_content_top(blocks)
    return [block for block in blocks if block.bottom >= content_top]


def detect_column_split(page: dict) -> float:
    width = page.get("width")
    if not isinstance(width, (int, float)):
        raise ValueError("Page width is missing or invalid.")
    return float(width) / 2


def split_columns(page: dict) -> tuple[list[TextBlock], list[TextBlock]]:
    split_x = detect_column_split(page)
    left: list[TextBlock] = []
    right: list[TextBlock] = []

    for block in content_text_blocks(page):
        if block.center_x < split_x:
            left.append(block)
        else:
            right.append(block)

    left.sort(key=lambda block: (block.top, block.x0, block.text))
    right.sort(key=lambda block: (block.top, block.x0, block.text))
    return left, right


def page_reading_order(page: dict) -> list[TextBlock]:
    left, right = split_columns(page)
    return [*left, *right]

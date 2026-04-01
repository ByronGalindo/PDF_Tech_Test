from __future__ import annotations

"""Grouping helpers for raw records inside section B.1."""

from dataclasses import dataclass

from unumbio_pdf_processing.layout import TextBlock, page_reading_order


RECORD_START_MARKER = "111"


@dataclass(frozen=True)
class RawRecord:
    """Sequence of blocks that belong to the same detected record."""

    start_page: int
    blocks: tuple[TextBlock, ...]

    @property
    def texts(self) -> list[str]:
        return [block.text for block in self.blocks]

    @property
    def pages(self) -> tuple[int, ...]:
        return tuple(sorted({block.page for block in self.blocks}))

    @property
    def block_count(self) -> int:
        return len(self.blocks)


def iter_b1_blocks(pages: list[dict]) -> list[TextBlock]:
    """Flatten the ordered blocks from all selected B.1 pages."""
    blocks: list[TextBlock] = []
    for page in pages:
        blocks.extend(page_reading_order(page))
    return blocks


def group_raw_records(pages: list[dict]) -> list[RawRecord]:
    """Start a new record every time the `111` INID marker appears."""
    blocks = iter_b1_blocks(pages)
    records: list[RawRecord] = []
    current_blocks: list[TextBlock] = []
    current_start_page: int | None = None

    for block in blocks:
        if block.text == RECORD_START_MARKER:
            if current_blocks:
                records.append(
                    RawRecord(
                        start_page=current_start_page or current_blocks[0].page,
                        blocks=tuple(current_blocks),
                    )
                )
            current_blocks = [block]
            current_start_page = block.page
            continue

        if current_blocks:
            current_blocks.append(block)

    if current_blocks:
        records.append(
            RawRecord(
                start_page=current_start_page or current_blocks[0].page,
                blocks=tuple(current_blocks),
            )
        )

    return records


def summarize_raw_record(record: RawRecord, sample_size: int = 16) -> dict:
    """Return a compact preview of a raw grouped record."""
    return {
        "_PAGE": record.start_page,
        "block_count": len(record.blocks),
        "sample": record.texts[:sample_size],
    }

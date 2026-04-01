from __future__ import annotations

from dataclasses import dataclass

from unumbio_pdf_processing.layout import TextBlock, page_reading_order


RECORD_START_MARKER = "111"


@dataclass(frozen=True)
class RawRecord:
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
    blocks: list[TextBlock] = []
    for page in pages:
        blocks.extend(page_reading_order(page))
    return blocks


def group_raw_records(pages: list[dict]) -> list[RawRecord]:
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
    return {
        "_PAGE": record.start_page,
        "block_count": len(record.blocks),
        "sample": record.texts[:sample_size],
    }

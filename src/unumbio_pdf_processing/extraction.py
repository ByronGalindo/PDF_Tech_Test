from __future__ import annotations

"""Extraction helpers that map raw records into the target schema."""

from unumbio_pdf_processing.records import RawRecord


TARGET_SINGLE_FIELDS = ("111", "151", "450", "210")
TARGET_MULTI_FIELDS = ("400",)
TARGET_FIELDS = set(TARGET_SINGLE_FIELDS) | set(TARGET_MULTI_FIELDS)


def extract_record(record: RawRecord) -> dict:
    """Extract the expected INID fields from one grouped raw record."""
    extracted: dict[str, object] = {"_PAGE": record.start_page}

    current_field: str | None = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal current_field, buffer
        if not current_field or not buffer:
            buffer = []
            return

        if current_field in TARGET_MULTI_FIELDS:
            extracted[current_field] = list(buffer)
        else:
            extracted[current_field] = " ".join(buffer)

        buffer = []

    for text in record.texts:
        if text in TARGET_FIELDS:
            flush()
            current_field = text
            buffer = []
            continue

        if current_field is None:
            continue

        buffer.append(text)

    flush()
    return extracted


def extract_records(records: list[RawRecord]) -> list[dict]:
    """Extract all grouped records into JSON-ready dictionaries."""
    return [extract_record(record) for record in records]

from __future__ import annotations

"""Validation helpers for the extracted output records."""

import re
from collections import Counter


DATE_RE = re.compile(r"^\d{2}/\d{2}/\d{4}$")
REFERENCE_RE = re.compile(r"^\d{2}/\d{2}/\d{4} - \d{4}/\d{3} - [A-Z]\.\d$")
REQUIRED_FIELDS = ("_PAGE", "111", "151", "450", "210", "400")


def validate_record(record: dict) -> list[str]:
    """Return a list of structural issues found in one extracted record."""
    issues: list[str] = []

    for field in REQUIRED_FIELDS:
        if field not in record:
            issues.append(f"missing:{field}")

    if "_PAGE" in record and not isinstance(record["_PAGE"], int):
        issues.append("invalid:_PAGE")

    for field in ("111", "151", "450", "210"):
        value = record.get(field)
        if value is None:
            continue
        if not isinstance(value, str) or not value.strip():
            issues.append(f"invalid:{field}")

    for field in ("151", "450"):
        value = record.get(field)
        if isinstance(value, str) and value and not DATE_RE.fullmatch(value):
            issues.append(f"invalid_date:{field}")

    if isinstance(record.get("111"), str) and isinstance(record.get("210"), str):
        if record["111"] != record["210"]:
            issues.append("mismatch:111_210")

    field_400 = record.get("400")
    if not isinstance(field_400, list) or not field_400:
        issues.append("invalid:400")
    else:
        for line in field_400:
            if not isinstance(line, str) or not line.strip():
                issues.append("invalid:400_line")
                continue
            if not REFERENCE_RE.fullmatch(line):
                issues.append("unexpected_format:400_line")
                break

    return issues


def summarize_validation(records: list[dict]) -> dict:
    """Summarize validation issues and duplicate record numbers."""
    record_issues: list[dict] = []
    number_counts = Counter(
        record["111"]
        for record in records
        if isinstance(record.get("111"), str) and record.get("111")
    )
    duplicates = sorted(number for number, count in number_counts.items() if count > 1)

    for index, record in enumerate(records):
        issues = validate_record(record)
        if issues:
            record_issues.append(
                {
                    "index": index,
                    "_PAGE": record.get("_PAGE"),
                    "111": record.get("111"),
                    "issues": issues,
                }
            )

    return {
        "record_count": len(records),
        "records_with_issues": len(record_issues),
        "issue_examples": record_issues[:10],
        "duplicate_111_count": len(duplicates),
        "duplicate_111_examples": duplicates[:10],
    }

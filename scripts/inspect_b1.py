from __future__ import annotations

import json
from pathlib import Path

from unumbio_pdf_processing.inspection import DEFAULT_SOURCE, summarize_b1_range


def main() -> None:
    summary = summarize_b1_range(Path(DEFAULT_SOURCE))
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

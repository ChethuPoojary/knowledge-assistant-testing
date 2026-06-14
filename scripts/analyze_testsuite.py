from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from framework.config import REPORTS_DIR, TEST_SUITE_FILE
from framework.testsuite_loader import load_cases, validate_cases


def main() -> None:
    cases = load_cases(TEST_SUITE_FILE)
    validation = validate_cases(cases)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output = REPORTS_DIR / "testsuite_validation_summary.json"
    output.write_text(json.dumps(validation, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(validation, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

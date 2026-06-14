from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from framework.config import REPORTS_DIR, TEST_SUITE_FILE
from framework.testsuite_loader import load_cases, validate_cases


def _read_junit(path: Path) -> Counter:
    counts = Counter()
    if not path.exists():
        return counts
    root = ET.parse(path).getroot()
    for testcase in root.iter("testcase"):
        if testcase.find("skipped") is not None:
            counts["skipped"] += 1
        elif testcase.find("failure") is not None or testcase.find("error") is not None:
            counts["failed"] += 1
        else:
            counts["passed"] += 1
    return counts


def main() -> None:
    cases = load_cases(TEST_SUITE_FILE)
    validation = validate_cases(cases)
    per_sheet = defaultdict(lambda: {"cases": 0, "ui": 0, "api": 0, "passed": 0, "failed": 0, "skipped": 0})

    for case in cases:
        per_sheet[case.sheet]["cases"] += 1
        if case.is_ui:
            per_sheet[case.sheet]["ui"] += 1
        if case.is_api:
            per_sheet[case.sheet]["api"] += 1

    for sheet in per_sheet:
        safe = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in sheet)
        counts = _read_junit(REPORTS_DIR / "junit" / f"{safe}.xml")
        per_sheet[sheet].update({key: counts[key] for key in ("passed", "failed", "skipped")})

    totals = Counter()
    for item in per_sheet.values():
        totals["cases"] += item["cases"]
        totals["ui"] += item["ui"]
        totals["api"] += item["api"]
        totals["passed"] += item["passed"]
        totals["failed"] += item["failed"]
        totals["skipped"] += item["skipped"]

    executed = totals["passed"] + totals["failed"] + totals["skipped"]
    coverage = round((executed / (totals["ui"] + totals["api"])) * 100, 2) if (totals["ui"] + totals["api"]) else 0

    summary = {
        "total_sheets_processed": len(per_sheet),
        "total_test_cases_per_sheet": dict(per_sheet),
        "total_ui_test_cases": totals["ui"],
        "total_api_test_cases": totals["api"],
        "total_passed": totals["passed"],
        "total_failed": totals["failed"],
        "total_skipped": totals["skipped"],
        "coverage_percentage": coverage,
        "missing_or_ambiguous_scenarios": validation["findings"],
        "recommendations": [
            "Clarify cross-region home-region versus destination-region policy behavior.",
            "Define exact refusal wording expectations to reduce brittle assertion logic.",
            "Add stable data-testid attributes to UI controls for robust automation.",
            "Document the expected API schema for citations and document filtering.",
            "Separate exploratory/spec-gap rows from release-gating regression rows.",
        ],
        "assumptions_risks_blockers": [
            "UI automation uses resilient label/role-based selectors because no stable data-testid contract is available.",
            "Spec-gap scenarios are treated as service stability checks and documented behavior rather than strict pass/fail business assertions.",
            "Live service defects are reported as failed tests and preserved in Allure evidence.",
        ],
    }

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "consolidated_execution_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    md = [
        "# Consolidated Execution Summary",
        "",
        f"- Total sheets processed: {summary['total_sheets_processed']}",
        f"- Total UI test cases: {totals['ui']}",
        f"- Total API test cases: {totals['api']}",
        f"- Total passed: {totals['passed']}",
        f"- Total failed: {totals['failed']}",
        f"- Total skipped: {totals['skipped']}",
        f"- Coverage percentage: {coverage}%",
        "",
        "## Per-Sheet Results",
        "",
        "| Sheet | Cases | UI | API | Passed | Failed | Skipped |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for sheet, item in per_sheet.items():
        md.append(f"| {sheet} | {item['cases']} | {item['ui']} | {item['api']} | {item['passed']} | {item['failed']} | {item['skipped']} |")
    md.extend(["", "## Gaps, Ambiguities, Duplicates, Missing Edge Cases", ""])
    for finding in validation["findings"]:
        md.append(f"- **{finding['severity']} {finding['type']}** ({finding['sheet']} / {finding['test_case_id']}): {finding['detail']}")
    md.extend(["", "## Recommendations", ""])
    md.extend(f"- {item}" for item in summary["recommendations"])
    md.extend(["", "## Assumptions, Risks, Blockers", ""])
    md.extend(f"- {item}" for item in summary["assumptions_risks_blockers"])
    (REPORTS_DIR / "consolidated_execution_summary.md").write_text("\n".join(md), encoding="utf-8")
    print(REPORTS_DIR / "consolidated_execution_summary.md")


if __name__ == "__main__":
    main()

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

import openpyxl

from framework.models import TestCase


REQUIRED_COLUMNS = {
    "TC-ID",
    "Category",
    "Region",
    "Role",
    "Input Question / Prompt",
    "Expected Behavior",
    "Must NOT Do",
    "Pass Criteria",
    "Risk",
    "Testing Layer",
}


def _clean(value) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _find_header_row(rows: list[tuple]) -> int | None:
    for index, row in enumerate(rows):
        values = {_clean(value) for value in row}
        if "Testing Layer" in values and ("TC-ID" in values or "#" in values):
            return index
    return None


def load_cases(workbook_path: Path, include_param_matrix: bool = False) -> list[TestCase]:
    workbook = openpyxl.load_workbook(workbook_path, data_only=True)
    cases: list[TestCase] = []

    for worksheet in workbook.worksheets:
        if worksheet.title.startswith("📊"):
            continue
        if worksheet.title.startswith("🔢") and not include_param_matrix:
            continue

        rows = list(worksheet.iter_rows(values_only=True))
        header_index = _find_header_row(rows)
        if header_index is None:
            continue

        headers = [_clean(value) for value in rows[header_index]]
        for row_number, row in enumerate(rows[header_index + 1 :], start=header_index + 2):
            values = {headers[column]: _clean(row[column]) if column < len(row) else "" for column in range(len(headers)) if headers[column]}
            if not any(values.values()):
                continue

            test_case_id = values.get("TC-ID") or values.get("#")
            prompt = values.get("Input Question / Prompt") or values.get("Question")
            expected = values.get("Expected Behavior") or values.get("Expected Doc / REFUSE")
            if not test_case_id or not prompt:
                continue

            cases.append(
                TestCase(
                    sheet=worksheet.title,
                    row_number=row_number,
                    test_case_id=str(test_case_id),
                    category=values.get("Category") or worksheet.title,
                    region=values.get("Region"),
                    role=values.get("Role"),
                    prompt=prompt,
                    expected_behavior=expected,
                    must_not_do=values.get("Must NOT Do"),
                    pass_criteria=values.get("Pass Criteria") or expected,
                    risk=values.get("Risk"),
                    testing_layer=values.get("Testing Layer") or "Both",
                )
            )

    return cases


def validate_cases(cases: list[TestCase]) -> dict:
    findings: list[dict] = []
    seen = defaultdict(list)

    for case in cases:
        key = (case.sheet, case.test_case_id)
        seen[key].append(case.row_number)

        for field_name in ("region", "role", "prompt", "expected_behavior", "pass_criteria", "testing_layer"):
            if not getattr(case, field_name):
                findings.append(
                    {
                        "severity": "High",
                        "type": "Missing required value",
                        "sheet": case.sheet,
                        "test_case_id": case.test_case_id,
                        "detail": f"Missing {field_name}",
                    }
                )

        if case.testing_layer not in {"UI", "API", "Both"}:
            findings.append(
                {
                    "severity": "High",
                    "type": "Invalid testing layer",
                    "sheet": case.sheet,
                    "test_case_id": case.test_case_id,
                    "detail": f"Testing Layer must be UI, API, or Both. Found: {case.testing_layer}",
                }
            )

        if case.is_ui and not case.region:
            findings.append(
                {
                    "severity": "Medium",
                    "type": "UI selector ambiguity",
                    "sheet": case.sheet,
                    "test_case_id": case.test_case_id,
                    "detail": "UI case has no region value.",
                }
            )

        if re.search(r"SPEC GAP|ambig", f"{case.category} {case.expected_behavior}", re.I):
            findings.append(
                {
                    "severity": "Medium",
                    "type": "Specification gap",
                    "sheet": case.sheet,
                    "test_case_id": case.test_case_id,
                    "detail": "Expected behavior asks to document actual behavior rather than assert a product rule.",
                }
            )

    for (sheet, test_case_id), rows in seen.items():
        if len(rows) > 1:
            findings.append(
                {
                    "severity": "High",
                    "type": "Duplicate test case id",
                    "sheet": sheet,
                    "test_case_id": test_case_id,
                    "detail": f"Duplicate rows: {rows}",
                }
            )

    sheet_counts = Counter(case.sheet for case in cases)
    layer_counts = Counter(case.testing_layer for case in cases)
    return {
        "total_cases": len(cases),
        "sheet_counts": dict(sheet_counts),
        "layer_counts": dict(layer_counts),
        "findings": findings,
    }


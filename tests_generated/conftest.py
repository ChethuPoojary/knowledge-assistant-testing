from __future__ import annotations

import os
from pathlib import Path

import pytest

from framework.config import REPORTS_DIR, TEST_SUITE_FILE
from framework.testsuite_loader import load_cases


def pytest_addoption(parser):
    parser.addoption("--sheet", action="store", default=None, help="Run one workbook sheet by name.")


def pytest_generate_tests(metafunc):
    if "case" not in metafunc.fixturenames:
        return

    sheet_filter = metafunc.config.getoption("--sheet") or os.environ.get("KA_SHEET")
    layer = "ui" if "ui" in metafunc.module.__name__ else "api"
    cases = load_cases(TEST_SUITE_FILE)
    cases = [case for case in cases if (case.is_ui if layer == "ui" else case.is_api)]
    if sheet_filter:
        cases = [case for case in cases if case.sheet == sheet_filter]

    ids = [f"{case.sheet}::{case.test_case_id}" for case in cases]
    metafunc.parametrize("case", cases, ids=ids)


@pytest.fixture
def screenshot_dir() -> Path:
    path = REPORTS_DIR / "screenshots"
    path.mkdir(parents=True, exist_ok=True)
    return path


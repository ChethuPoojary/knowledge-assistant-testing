import allure
import pytest
from playwright.sync_api import sync_playwright

from framework.assertions import ApiEvidence, assert_api_case
from framework.config import AUTHOR
from framework.ui.pages import KnowledgeAssistantPage


def _attach_expected_result(case):
    expected = f"""Test Case ID: {case.test_case_id}
Feature/Sheet: {case.sheet}
Category: {case.category}
Region: {case.region}
Role: {case.role}
Prompt: {case.prompt}

Expected Behavior:
{case.expected_behavior}

Pass Criteria:
{case.pass_criteria}

Must Not Do:
{case.must_not_do}

Testing Layer: {case.testing_layer}
Risk: {case.risk}
"""
    allure.attach(expected, f"{case.test_case_id} - expected-result.txt", allure.attachment_type.TEXT)


def _attach_actual_result(case, page_text, status="Executed"):
    actual = f"""Test Case ID: {case.test_case_id}
Execution Status Before Assertion: {status}

Actual UI Response / Page Text:
{page_text}
"""
    allure.attach(actual, f"{case.test_case_id} - actual-result.txt", allure.attachment_type.TEXT)


@allure.epic("Knowledge Assistant")
@allure.label("owner", AUTHOR)
@allure.label("tester", AUTHOR)
@allure.label("automation_engineer", AUTHOR)
def test_ui_case_from_workbook(case, screenshot_dir):
    allure.dynamic.feature(case.sheet)
    allure.dynamic.story(case.category)
    allure.dynamic.title(f"{case.test_case_id} - UI - {case.prompt}")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        assistant_page = KnowledgeAssistantPage(page, screenshot_dir)

        try:
            with allure.step("Navigate to Knowledge Assistant"):
                assistant_page.open(case)
            with allure.step("Set user region and role"):
                assistant_page.set_context(case)
            with allure.step("Submit prompt and capture UI response"):
                page_text = assistant_page.ask_question(case)
            with allure.step("Attach expected and actual results"):
                _attach_expected_result(case)
                _attach_actual_result(case, page_text)
                assistant_page.capture_evidence(case, "expected-actual-evidence")
            with allure.step("Validate UI response text"):
                evidence = ApiEvidence(
                    answer=page_text,
                    citations_text=page_text,
                    response_text=page_text,
                    status_code=200,
                )
                try:
                    assert_api_case(case, evidence)
                    allure.attach(
                        "Validation Result: PASSED",
                        f"{case.test_case_id} - validation-result.txt",
                        allure.attachment_type.TEXT,
                    )
                    assistant_page.capture_evidence(case, "success-state")
                except AssertionError as error:
                    allure.attach(
                        f"Validation Result: FAILED\n\nError:\n{error}",
                        f"{case.test_case_id} - validation-result.txt",
                        allure.attachment_type.TEXT,
                    )
                    assistant_page.capture_evidence(case, "failure-state")
                    pytest.fail(str(error), pytrace=True)
        finally:
            browser.close()

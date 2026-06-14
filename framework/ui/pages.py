from __future__ import annotations

import re
from pathlib import Path

import allure
from playwright.sync_api import Page, expect

from framework.api_client import normalize_prompt
from framework.config import BASE_URL
from framework.models import TestCase


class KnowledgeAssistantPage:
    def __init__(self, page: Page, screenshot_dir: Path):
        self.page = page
        self.screenshot_dir = screenshot_dir
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)

    def open(self, case: TestCase) -> None:
        self.page.goto(BASE_URL, wait_until="domcontentloaded")
        self._screenshot(case, "navigation-home")

    def set_context(self, case: TestCase) -> None:
        self._select_value(["region", "select region"], case.region)
        self._select_value(["role", "select role"], case.role)
        self._screenshot(case, "set-region-role")

    def ask_question(self, case: TestCase) -> str:
        prompt = normalize_prompt(case.prompt)
        textbox = self.page.get_by_role("textbox").first
        textbox.fill(prompt)
        self._screenshot(case, "enter-question")

        button = self.page.get_by_role("button", name=re.compile("ask|submit|send|query", re.I)).first
        button.click()
        self.page.wait_for_load_state("networkidle")
        self._screenshot(case, "submit-question")

        body_text = self.page.locator("body").inner_text(timeout=10000)
        allure.attach(body_text, "ui-page-text.txt", allure.attachment_type.TEXT)
        self._screenshot(case, "validation-state")
        return body_text

    def capture_evidence(self, case: TestCase, label: str) -> None:
        self._screenshot(case, label)

    def _select_value(self, label_patterns: list[str], value: str) -> None:
        if not value:
            return
        for pattern in label_patterns:
            try:
                self.page.get_by_label(re.compile(pattern, re.I)).select_option(value, timeout=1500)
                return
            except Exception:
                pass
        try:
            self.page.locator("select").filter(has_text=re.compile(value, re.I)).select_option(value, timeout=1500)
            return
        except Exception:
            pass
        option = self.page.get_by_role("option", name=re.compile(re.escape(value), re.I))
        if option.count() > 0:
            option.first.click()
            return
        expect(self.page.get_by_text(value, exact=False).first).to_be_visible(timeout=3000)

    def _screenshot(self, case: TestCase, label: str) -> None:
        safe_id = re.sub(r"[^A-Za-z0-9_.-]+", "_", case.test_case_id)
        path = self.screenshot_dir / f"{safe_id}_{label}.png"
        self.page.screenshot(path=str(path), full_page=True)
        allure.attach.file(str(path), name=f"{case.test_case_id} - {label}", attachment_type=allure.attachment_type.PNG)

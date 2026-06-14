from __future__ import annotations

import requests

from framework.config import BASE_URL
from framework.models import TestCase


class KnowledgeAssistantApiClient:
    def __init__(self, base_url: str = BASE_URL, timeout: int = 20):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def query(self, case: TestCase) -> requests.Response:
        payload = {
            "question": normalize_prompt(case.prompt),
            "region": case.region,
            "role": case.role,
        }
        return self.session.post(f"{self.base_url}/query", json=payload, timeout=self.timeout)

    def documents(self, case: TestCase) -> requests.Response:
        return self.session.get(
            f"{self.base_url}/documents",
            params={"region": case.region, "role": case.role},
            timeout=self.timeout,
        )


def normalize_prompt(prompt: str) -> str:
    value = (prompt or "").strip()
    if value.lower() == "(empty string)":
        return ""
    if value.lower() == "(whitespace only)":
        return "   "
    return value


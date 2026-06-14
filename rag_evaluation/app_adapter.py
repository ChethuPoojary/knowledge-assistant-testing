from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any

import requests

from framework.api_client import KnowledgeAssistantApiClient, normalize_prompt
from framework.models import TestCase


@dataclass
class RagAppResult:
    test_case_id: str
    sheet: str
    category: str
    region: str
    role: str
    question: str
    expected_answer: str
    answer: str
    contexts: list[str]
    citations: list[str]
    status_code: int
    latency_ms: float
    request_payload: dict[str, Any]
    response_payload: Any
    response_text: str
    error: str = ""


class KnowledgeAssistantRagAdapter:
    def __init__(self, base_url: str, timeout_seconds: int = 30):
        self.client = KnowledgeAssistantApiClient(base_url=base_url, timeout=timeout_seconds)
        self.session = requests.Session()
        self.timeout_seconds = timeout_seconds

    def evaluate_case(self, case: TestCase) -> RagAppResult:
        question = normalize_prompt(case.prompt)
        request_payload = {"question": question, "region": case.region, "role": case.role}
        started = time.perf_counter()
        error = ""
        response_text = ""
        status_code = 0
        body: Any = {}

        try:
            response = self.client.query(case)
            latency_ms = (time.perf_counter() - started) * 1000
            status_code = response.status_code
            response_text = response.text
            try:
                body = response.json()
            except ValueError:
                body = response.text
        except Exception as exc:
            latency_ms = (time.perf_counter() - started) * 1000
            error = repr(exc)

        answer = self._extract_answer(body)
        citations = self._extract_citations(body)
        contexts = self._extract_contexts(body)
        if not contexts:
            contexts = self._fetch_visible_document_contexts(case)

        return RagAppResult(
            test_case_id=case.test_case_id,
            sheet=case.sheet,
            category=case.category,
            region=case.region,
            role=case.role,
            question=question,
            expected_answer=case.expected_behavior or case.pass_criteria,
            answer=answer,
            contexts=contexts,
            citations=citations,
            status_code=status_code,
            latency_ms=latency_ms,
            request_payload=request_payload,
            response_payload=body,
            response_text=response_text,
            error=error,
        )

    def _fetch_visible_document_contexts(self, case: TestCase) -> list[str]:
        try:
            response = self.client.documents(case)
            if response.status_code >= 400:
                return []
            body = response.json()
            if isinstance(body, list):
                return [self._document_to_text(item) for item in body if item]
            if isinstance(body, dict):
                documents = body.get("documents") or body.get("data") or body.get("results") or []
                if isinstance(documents, list):
                    return [self._document_to_text(item) for item in documents if item]
                return [json.dumps(body, ensure_ascii=False)]
        except Exception:
            return []
        return []

    @staticmethod
    def _extract_answer(body: Any) -> str:
        if isinstance(body, dict):
            for key in ("answer", "response", "result", "message", "output"):
                if body.get(key) is not None:
                    return str(body[key])
            return json.dumps(body, ensure_ascii=False)
        return str(body or "")

    @staticmethod
    def _extract_citations(body: Any) -> list[str]:
        if not isinstance(body, dict):
            return []
        citations = body.get("citations") or body.get("sources") or body.get("references") or []
        if isinstance(citations, list):
            return [str(item.get("id") or item.get("doc_id") or item) if isinstance(item, dict) else str(item) for item in citations]
        return [str(citations)] if citations else []

    @classmethod
    def _extract_contexts(cls, body: Any) -> list[str]:
        if not isinstance(body, dict):
            return []
        contexts = body.get("contexts") or body.get("retrieved_contexts") or body.get("source_documents") or body.get("documents") or []
        if isinstance(contexts, list):
            return [cls._document_to_text(item) for item in contexts if item]
        if contexts:
            return [str(contexts)]
        return []

    @staticmethod
    def _document_to_text(document: Any) -> str:
        if isinstance(document, str):
            return document
        if isinstance(document, dict):
            parts = []
            for key in ("id", "doc_id", "title", "name", "content", "text", "body", "summary"):
                if document.get(key):
                    parts.append(f"{key}: {document[key]}")
            return "\n".join(parts) if parts else json.dumps(document, ensure_ascii=False)
        return str(document)

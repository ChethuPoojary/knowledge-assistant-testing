import csv
from pathlib import Path

import allure
import pytest
import requests


BASE_URL = "https://main-knowledge-assistant.newpage.workers.dev"
DATA_FILE = Path(__file__).resolve().parents[1] / "test-data" / "golden_questions.csv"
RESTRICTED_DOCUMENTS = {"D-003", "D-005", "D-009"}


def load_golden_questions():
    with DATA_FILE.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def case_id(case):
    return f"{case['region']}-{case['role']}-{case['question'][:45]}"


def normalize_citations(citations):
    if isinstance(citations, list):
        return " ".join(str(citation) for citation in citations)
    return str(citations or "")


def attach_response(response):
    allure.attach(
        response.text,
        name="api-response.json",
        attachment_type=allure.attachment_type.JSON,
    )


@allure.epic("Knowledge Assistant")
@allure.feature("Golden question API regression")
@pytest.mark.parametrize("case", load_golden_questions(), ids=case_id)
def test_query_matches_expected_outcome(case):
    payload = {
        "question": case["question"],
        "region": case["region"],
        "role": case["role"],
    }

    allure.dynamic.title(case["question"])
    allure.dynamic.description(
        f"Region: {case['region']}\n"
        f"Role: {case['role']}\n"
        f"Expected document: {case['expected_document']}\n"
        f"Expected outcome: {case['expected_outcome']}"
    )

    with allure.step("Send query request"):
        response = requests.post(f"{BASE_URL}/query", json=payload, timeout=20)
        attach_response(response)
        assert response.status_code == 200

    body = response.json()
    answer = str(body.get("answer", ""))
    citation_text = normalize_citations(body.get("citations", []))

    with allure.step("Validate answer and citations"):
        if case["expected_document"] != "None":
            assert case["expected_document"] in citation_text, (
                f"Expected citation {case['expected_document']}, got: {citation_text or 'no citations'}"
            )
            assert case["expected_outcome"].lower() in answer.lower(), (
                f"Expected answer to contain {case['expected_outcome']!r}, got: {answer!r}"
            )
        else:
            leaked_in_answer = sorted(document for document in RESTRICTED_DOCUMENTS if document in answer)
            leaked_in_citations = sorted(document for document in RESTRICTED_DOCUMENTS if document in citation_text)
            assert not leaked_in_answer, f"Restricted document leaked in answer: {leaked_in_answer}"
            assert not leaked_in_citations, f"Restricted document leaked in citations: {leaked_in_citations}"


@allure.epic("Knowledge Assistant")
@allure.feature("Document lifecycle filtering")
def test_documents_endpoint_excludes_non_approved_documents():
    with allure.step("Request visible APAC employee documents"):
        response = requests.get(
            f"{BASE_URL}/documents",
            params={"region": "APAC", "role": "Employee"},
            timeout=20,
        )
        attach_response(response)
        assert response.status_code == 200

    documents = response.json()
    document_text = str(documents)
    with allure.step("Validate restricted lifecycle documents are hidden"):
        assert "D-003" not in document_text
        assert "Draft" not in document_text
        assert "In Review" not in document_text
        assert "Retired" not in document_text

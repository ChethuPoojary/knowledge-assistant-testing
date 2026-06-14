import csv
from pathlib import Path

import pytest
import requests


BASE_URL = "https://main-knowledge-assistant.newpage.workers.dev"
DATA_FILE = Path(__file__).resolve().parents[1] / "test-data" / "golden_questions.csv"


def load_golden_questions():
    with DATA_FILE.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


@pytest.mark.parametrize("case", load_golden_questions())
def test_query_matches_expected_outcome(case):
    payload = {
        "question": case["question"],
        "region": case["region"],
        "role": case["role"],
    }

    response = requests.post(f"{BASE_URL}/query", json=payload, timeout=20)
    assert response.status_code == 200

    body = response.json()
    answer = str(body.get("answer", ""))
    citations = body.get("citations", [])
    citation_text = " ".join(str(citation) for citation in citations)

    if case["expected_document"] != "None":
        assert case["expected_document"] in citation_text
        assert case["expected_outcome"].lower() in answer.lower()
    else:
        restricted_documents = ["D-003", "D-005", "D-009"]
        assert all(document not in answer for document in restricted_documents)
        assert all(document not in citation_text for document in restricted_documents)


def test_documents_endpoint_excludes_non_approved_documents():
    response = requests.get(
        f"{BASE_URL}/documents",
        params={"region": "APAC", "role": "Employee"},
        timeout=20,
    )
    assert response.status_code == 200

    documents = response.json()
    document_text = str(documents)
    assert "D-003" not in document_text
    assert "Draft" not in document_text
    assert "In Review" not in document_text
    assert "Retired" not in document_text


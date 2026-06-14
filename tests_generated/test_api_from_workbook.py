import json

import allure

from framework.api_client import KnowledgeAssistantApiClient
from framework.assertions import assert_api_case, build_evidence
from framework.config import AUTHOR


@allure.epic("Knowledge Assistant")
@allure.label("owner", AUTHOR)
@allure.label("tester", AUTHOR)
@allure.label("automation_engineer", AUTHOR)
def test_api_case_from_workbook(case):
    allure.dynamic.feature(case.sheet)
    allure.dynamic.story(case.category)
    allure.dynamic.title(f"{case.test_case_id} - {case.prompt}")
    allure.dynamic.description(
        f"Risk: {case.risk}\n"
        f"Region: {case.region}\n"
        f"Role: {case.role}\n"
        f"Expected: {case.expected_behavior}\n"
        f"Pass Criteria: {case.pass_criteria}\n"
        f"Must NOT Do: {case.must_not_do}"
    )

    client = KnowledgeAssistantApiClient()
    with allure.step("Prepare API request data"):
        request_details = {
            "test_case_id": case.test_case_id,
            "sheet": case.sheet,
            "region": case.region,
            "role": case.role,
            "prompt": case.prompt,
        }
        allure.attach(json.dumps(request_details, indent=2), "request-data.json", allure.attachment_type.JSON)

    with allure.step("Execute API request"):
        if case.prompt.strip().upper().startswith("GET /DOCUMENTS"):
            response = client.documents(case)
        else:
            response = client.query(case)

        allure.attach(str(response.status_code), "status-code.txt", allure.attachment_type.TEXT)
        allure.attach(json.dumps(dict(response.headers), indent=2), "response-headers.json", allure.attachment_type.JSON)
        allure.attach(response.text, "response-payload.json", allure.attachment_type.JSON)

    with allure.step("Validate API response"):
        try:
            body = response.json()
        except ValueError:
            body = response.text
        evidence = build_evidence(response.status_code, response.text, body)
        assert_api_case(case, evidence)


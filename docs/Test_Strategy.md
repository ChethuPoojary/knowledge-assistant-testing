# Test Strategy

## Objective

The goal of this assignment is to test the Knowledge Assistant as a black-box RAG-style application. The assistant answers employee questions from a controlled content library and must enforce document visibility based on region, role, and lifecycle state. The highest-risk failures are not normal application crashes, but incorrect or unsafe answers: unsupported claims, wrong citations, retired/draft/in-review content surfacing, or access boundaries being crossed.

## Risk-Based Prioritization

I prioritized scenarios where a defect could mislead an employee or expose information that should not be available:

- **Citation correctness:** answers must cite the correct approved source document. A correct-looking answer with a wrong citation is still a defect.
- **Lifecycle enforcement:** Draft, In Review, and Retired documents must not be used as authoritative sources.
- **Region boundaries:** region-specific policies such as Americas, EMEA, and APAC travel rules must not leak across regions.
- **Role boundaries:** Engineering, Finance, and Manager-only content must not be shown to general employees.
- **Hallucination and unsupported claims:** the assistant should refuse or redirect when approved content is unavailable.
- **Prompt-injection resistance:** adversarial prompts must not cause hidden, retired, draft, or unauthorized content to surface.
- **API/UI consistency:** the API response and UI rendering should agree on answer, citation, and visible documents.

## Test Design

The suite is driven by a golden-question workbook located in:

`test-suite/KnowledgeAssistant_TestSuite.xlsx`

Each sheet represents a feature area, such as happy path, lifecycle, role boundary, region boundary, citation, hallucination, security, edge cases, cross-region behavior, and API-vs-UI consistency. Each test case includes region, role, prompt, expected behavior, must-not-do rules, pass criteria, risk, and testing layer.

The golden-question suite intentionally avoids brittle exact-string assertions. Instead, assertions focus on durable product rules:

- required document IDs appear or do not appear;
- expected policy values such as `USD 75`, `EUR 60`, `3 days`, or `CFO` appear;
- forbidden values or restricted document IDs do not appear;
- refusals are accepted when no approved authorized source exists;
- service should not crash on edge/spec-gap scenarios.

## Layering Strategy

### API Layer

The API layer is the primary regression layer because it is faster, cheaper, and closer to the access and retrieval rules. API tests cover:

- role and region access rules;
- lifecycle exclusion;
- citation correctness;
- approved document use;
- documents endpoint scoping;
- negative and adversarial inputs;
- API behavior for both API-only and Both-layer test cases.

### UI Layer

The UI layer is used for behavior that must be verified in the browser:

- region and role selector behavior;
- prompt submission flow;
- rendered answer text;
- rendered citations;
- visible documents panel scoping;
- screenshot evidence for each major step;
- UI-specific failures and API-vs-UI differences.

The UI tests reuse the same golden-question data but are limited to UI and Both-layer cases to avoid duplicating all API checks in a slower browser layer.

## Automation Architecture

The automation framework uses:

- `pytest` for test execution;
- `requests` for API testing;
- Playwright for UI testing;
- Page Object Model for UI interactions;
- reusable API adapter/client code;
- workbook-driven parameterization;
- Allure reporting with request/response evidence and UI screenshots;
- generated defect reports and final defect summary workbooks.

Reports are generated under `reports/`, including API, UI, sheet-level reports, defect reports, and final summaries.

## Scope Not Fully Covered

The following items were intentionally deprioritized or treated as optional due to time:

- full load and stress testing;
- long-running drift monitoring;
- browser/device compatibility matrix;
- scheduled CI monitoring over time;
- complete performance benchmarking under concurrent users.

An optional RAG evaluation framework was added using RAGAS/custom metrics, but judge-based RAGAS metrics require a valid OpenAI API key with quota.

## Completion Criteria

The assignment is considered complete when:

- API and UI tests can run from the repository;
- test cases are data-driven from the golden-question workbook;
- Allure reports are generated and openable from file explorer;
- failed API/UI/Both defects are documented with expected vs actual results;
- UI failures include screenshot evidence;
- final defect summary deduplicates issues using `Execution Layer + Test Case ID`;
- README provides clear setup, execution, and report-opening instructions.

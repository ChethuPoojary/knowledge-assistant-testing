# Knowledge Assistant Testing Repository

This repository contains QA deliverables for the Knowledge Assistant take-home assignment. The assignment focuses on testing a RAG-based GenAI assistant that answers employee questions from internal company documents while enforcing region, role, and document lifecycle restrictions.

## Repository Structure

```text
knowledge-assistant-testing/
├── README.md
├── docs/
│   ├── Test_Strategy.md
│   ├── Test_Plan.md
│   ├── Risk_Assessment.md
│   ├── Reflection.md
│   └── RTM.md
├── test-data/
│   └── golden_questions.csv
├── test-cases/
│   └── Test_Cases.md
├── defects/
│   ├── BUG-001_Lifecycle_Leakage.md
│   ├── BUG-002_Citation_Mismatch.md
│   └── BUG-003_Prompt_Injection.md
├── api-tests/
│   └── test_knowledge_assistant_api.py
├── ui-tests/
│   └── knowledge-assistant.spec.ts
├── reports/
│   └── Test_Execution_Report.md
└── evidence/
    ├── screenshots/
    └── api_responses/
```

## Environment

- Base URL: `https://main-knowledge-assistant.newpage.workers.dev/`
- Supported regions: Americas, EMEA, APAC
- Supported roles: Employee, Engineering, Finance, Manager

## Setup

```bash
git clone https://github.com/ChethuPoojary/knowledge-assistant-testing.git
cd knowledge-assistant-testing
```

## Run API Tests

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest api-tests -v
```

## Run UI Tests

```bash
npm install
npx playwright install
npx playwright test
```

## Deliverables

- Test strategy
- Test plan
- Risk assessment
- Requirement traceability matrix
- Golden question dataset
- Manual test cases
- API automation suite
- UI automation suite
- Defect reports
- Execution report
- Reflection document


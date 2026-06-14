# Knowledge Assistant QA Automation

This repository contains the QA deliverables for the Newpage Solutions Knowledge Assistant take-home assignment. The application under test is a RAG-style assistant hosted at:

`https://main-knowledge-assistant.newpage.workers.dev/`

The suite verifies the assistant across API and UI layers using a golden-question workbook, automated tests, Allure reports, defect reports, and optional RAG evaluation.

## What Is Included

- Test strategy: `docs/Test_Strategy.md`
- Reflection: `docs/Reflection.md`
- Golden-question workbook: `test-suite/KnowledgeAssistant_TestSuite.xlsx`
- API automation: `tests_generated/test_api_from_workbook.py`
- UI automation: `tests_generated/test_ui_from_workbook.py`
- Framework utilities: `framework/`
- RAGAS/custom RAG evaluation: `rag_evaluation/`
- Allure reports: `reports/`
- Defect reports: `reports/defect-report*`
- Final defect summary: `reports/final-defect-summary/Final_Defect_Summary_Chethan_Poojary.xlsx`

## Test Deliverables Index

Use this section as the main reviewer/interviewer navigation list.

| Deliverable | File / Folder Name | Location |
| --- | --- | --- |
| Test Strategy | `Test_Strategy.md` | `docs/Test_Strategy.md` |
| Reflection | `Reflection.md` | `docs/Reflection.md` |
| Test Plan | `Test_Plan.md` | `docs/Test_Plan.md` |
| Risk Assessment | `Risk_Assessment.md` | `docs/Risk_Assessment.md` |
| Golden Question Test Suite | `KnowledgeAssistant_TestSuite.xlsx` | `test-suite/KnowledgeAssistant_TestSuite.xlsx` |
| API Automation Test File | `test_api_from_workbook.py` | `tests_generated/test_api_from_workbook.py` |
| UI Automation Test File | `test_ui_from_workbook.py` | `tests_generated/test_ui_from_workbook.py` |
| API Runner Script | `run_generated_api_allure.ps1` | `run_generated_api_allure.ps1` |
| UI Runner Script | `run_generated_ui_allure.ps1` | `run_generated_ui_allure.ps1` |
| Full Workbook Runner Script | `run_workbook_tests_allure.ps1` | `run_workbook_tests_allure.ps1` |
| API Allure Report | `index.html` | `reports/allure-report-api/index.html` |
| UI Allure Report | `index.html` | `reports/allure-report-ui/index.html` |
| Sheet-Level Allure Reports | per-sheet `index.html` files | `reports/allure-reports-by-sheet/` |
| Consolidated Execution Summary | `consolidated_execution_summary.md` | `reports/consolidated_execution_summary.md` |
| UI Defect Report | `Latest_UI_Defect_Report_Chethan_Poojary.xlsx` | `reports/defect-report/Latest_UI_Defect_Report_Chethan_Poojary.xlsx` |
| API Defect Report | `Latest_API_Defect_Report_Chethan_Poojary.xlsx` | `reports/defect-report-api/Latest_API_Defect_Report_Chethan_Poojary.xlsx` |
| Both Execution Defect Report | `Latest_Both_Execution_Defect_Report_Chethan_Poojary.xlsx` | `reports/defect-report-both/Latest_Both_Execution_Defect_Report_Chethan_Poojary.xlsx` |
| Final Defect Summary | `Final_Defect_Summary_Chethan_Poojary.xlsx` | `reports/final-defect-summary/Final_Defect_Summary_Chethan_Poojary.xlsx` |
| UI Failure Screenshots | screenshot PNG files | `reports/screenshots/` |
| RAGAS Evaluation Runner | `run_ragas_evaluation.ps1` | `run_ragas_evaluation.ps1` |
| RAGAS Setup Check | `check_ragas_setup.py` | `check_ragas_setup.py` |
| RAG Evaluation Framework | Python package | `rag_evaluation/` |
| RAG Evaluation Report | `index.html` | `reports/ragas-evaluation/index.html` |
| RAG Evaluation Results CSV | `rag_evaluation_results.csv` | `reports/ragas-evaluation/rag_evaluation_results.csv` |
| Custom RAG Metrics CSV | `custom_metrics.csv` | `reports/ragas-evaluation/custom_metrics.csv` |
| Raw RAG App Responses | `raw_app_responses.csv` | `reports/ragas-evaluation/raw_app_responses.csv` |
| RAG Evaluation Summary | `summary.md` / `summary.json` | `reports/ragas-evaluation/` |

Recommended review order:

1. `docs/Test_Strategy.md`
2. `test-suite/KnowledgeAssistant_TestSuite.xlsx`
3. `tests_generated/test_api_from_workbook.py`
4. `tests_generated/test_ui_from_workbook.py`
5. `reports/allure-report-api/index.html`
6. `reports/allure-report-ui/index.html`
7. `reports/final-defect-summary/Final_Defect_Summary_Chethan_Poojary.xlsx`
8. `docs/Reflection.md`

## Where API, UI, and Both Test Cases Are Added

All functional test cases are maintained in the golden-question workbook:

```powershell
test-suite\KnowledgeAssistant_TestSuite.xlsx
```

The workbook has a `Testing Layer` column. This column decides which automation file executes the test case:

| Testing Layer Value | Test Case Location | Executed By | Folder |
| --- | --- | --- | --- |
| `API` | `test-suite/KnowledgeAssistant_TestSuite.xlsx` | `test_api_from_workbook.py` | `tests_generated/` |
| `UI` | `test-suite/KnowledgeAssistant_TestSuite.xlsx` | `test_ui_from_workbook.py` | `tests_generated/` |
| `Both` | `test-suite/KnowledgeAssistant_TestSuite.xlsx` | Both `test_api_from_workbook.py` and `test_ui_from_workbook.py` | `tests_generated/` |

Automation files:

```powershell
tests_generated\test_api_from_workbook.py
tests_generated\test_ui_from_workbook.py
tests_generated\conftest.py
```

Supporting framework files:

```powershell
framework\testsuite_loader.py
framework\api_client.py
framework\assertions.py
framework\ui\pages.py
```

Execution scripts:

```powershell
run_generated_api_allure.ps1
run_generated_ui_allure.ps1
run_workbook_tests_allure.ps1
```

## Setup

Open PowerShell and run:

```powershell
cd C:\Users\sam\Knowledge-Assistant-Test
python -m pip install -r requirements.txt
python -m playwright install chromium
```

All commands below should be executed from:

```powershell
C:\Users\sam\Knowledge-Assistant-Test
```

## Run API Tests

```powershell
powershell -ExecutionPolicy Bypass -File .\run_generated_api_allure.ps1
```

API report:

```powershell
C:\Users\sam\Knowledge-Assistant-Test\reports\allure-report-api\index.html
```

This report is generated as a single-file Allure report, so it can be opened directly from File Explorer.

## Run UI Tests

```powershell
powershell -ExecutionPolicy Bypass -File .\run_generated_ui_allure.ps1
```

UI report:

```powershell
C:\Users\sam\Knowledge-Assistant-Test\reports\allure-report-ui\index.html
```

The UI report includes screenshots, expected result, actual result, and validation evidence for each test.

## Run All Workbook Tests By Sheet

```powershell
powershell -ExecutionPolicy Bypass -File .\run_workbook_tests_allure.ps1
```

Sheet-level reports:

```powershell
C:\Users\sam\Knowledge-Assistant-Test\reports\allure-reports-by-sheet
```

Consolidated summary:

```powershell
C:\Users\sam\Knowledge-Assistant-Test\reports\consolidated_execution_summary.md
```

## Defect Reports

Generated defect reports are available here:

```powershell
C:\Users\sam\Knowledge-Assistant-Test\reports\defect-report
C:\Users\sam\Knowledge-Assistant-Test\reports\defect-report-api
C:\Users\sam\Knowledge-Assistant-Test\reports\defect-report-both
C:\Users\sam\Knowledge-Assistant-Test\reports\final-defect-summary
```

Important files:

```powershell
reports\defect-report\Latest_UI_Defect_Report_Chethan_Poojary.xlsx
reports\defect-report-api\Latest_API_Defect_Report_Chethan_Poojary.xlsx
reports\defect-report-both\Latest_Both_Execution_Defect_Report_Chethan_Poojary.xlsx
reports\final-defect-summary\Final_Defect_Summary_Chethan_Poojary.xlsx
```

The final defect summary removes duplicate defects using this key:

`Execution Layer + Test Case ID`

If the same test case fails in both API and UI, it is counted as two separate issues because API and UI are separate execution layers.

Latest execution summary:

| Execution | Executed | Passed | Failed | Skipped |
| --- | ---: | ---: | ---: | ---: |
| API | 69 | 33 | 36 | 0 |
| UI | 45 | 20 | 25 | 0 |
| Both | 114 | 53 | 61 | 0 |

## Optional RAGAS Evaluation

The repository includes an optional RAG evaluation framework. Custom metrics run without an evaluator API key. RAGAS judge metrics require an OpenAI API key with active quota.

Set the API key in the same PowerShell window:

```powershell
$env:OPENAI_API_KEY="paste_your_openai_api_key_here"
```

Check setup:

```powershell
python .\check_ragas_setup.py
```

Run RAG evaluation:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ragas_evaluation.ps1
```

RAG evaluation report:

```powershell
C:\Users\sam\Knowledge-Assistant-Test\reports\ragas-evaluation\index.html
```

If OpenAI quota is unavailable, RAGAS judge metrics may fail with `429 insufficient_quota`. In that case, billing/quota must be fixed in the OpenAI account, or the evaluation can be run with custom metrics only.

## Notes

- Some tests are currently failing because they identify product defects in the hosted assistant.
- Failed API and UI cases are documented in the defect reports.
- UI failures include screenshot evidence.
- Reports are regenerated when the corresponding run script is executed.

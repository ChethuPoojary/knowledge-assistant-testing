# Requirement Traceability Matrix

| Requirement Area | Golden Suite Coverage | API Automation | UI Automation | Report Evidence |
| --- | --- | --- | --- | --- |
| Happy path answers and citations | `1_HappyPath` | `tests_generated/test_api_from_workbook.py` | `tests_generated/test_ui_from_workbook.py` | `reports/allure-reports-by-sheet/1_HappyPath/index.html` |
| Document lifecycle exclusion | `2_Lifecycle` | `tests_generated/test_api_from_workbook.py` | `tests_generated/test_ui_from_workbook.py` | `reports/allure-reports-by-sheet/2_Lifecycle/index.html` |
| Role-based access boundaries | `3_RoleBoundary` | `tests_generated/test_api_from_workbook.py` | `tests_generated/test_ui_from_workbook.py` | `reports/allure-reports-by-sheet/3_RoleBoundary/index.html` |
| Region-based access boundaries | `4_RegionBoundary` | `tests_generated/test_api_from_workbook.py` | `tests_generated/test_ui_from_workbook.py` | `reports/allure-reports-by-sheet/4_RegionBoundary/index.html` |
| Citation correctness | `5_Citation` | `tests_generated/test_api_from_workbook.py` | `tests_generated/test_ui_from_workbook.py` | `reports/allure-reports-by-sheet/5_Citation/index.html` |
| Hallucination and unsupported answer handling | `6_Hallucination` | `tests_generated/test_api_from_workbook.py` | `tests_generated/test_ui_from_workbook.py` | `reports/allure-reports-by-sheet/6_Hallucination/index.html` |
| Prompt injection / security behavior | `7_Security` | `tests_generated/test_api_from_workbook.py` | `tests_generated/test_ui_from_workbook.py` | `reports/allure-reports-by-sheet/7_Security/index.html` |
| Edge cases and malformed inputs | `8_EdgeCases` | `tests_generated/test_api_from_workbook.py` | `tests_generated/test_ui_from_workbook.py` | `reports/allure-reports-by-sheet/8_EdgeCases/index.html` |
| Cross-region behavior | `9_CrossRegion` | `tests_generated/test_api_from_workbook.py` | `tests_generated/test_ui_from_workbook.py` | `reports/allure-reports-by-sheet/9_CrossRegion/index.html` |
| API vs UI consistency | `10_APIvsUI` | `tests_generated/test_api_from_workbook.py` | `tests_generated/test_ui_from_workbook.py` | `reports/allure-reports-by-sheet/10_APIvsUI/index.html` |

Final defect and execution evidence:

- API defects: `reports/defect-report-api/Latest_API_Defect_Report_Chethan_Poojary.xlsx`
- UI defects: `reports/defect-report/Latest_UI_Defect_Report_Chethan_Poojary.xlsx`
- Both-layer defects: `reports/defect-report-both/Latest_Both_Execution_Defect_Report_Chethan_Poojary.xlsx`
- Final deduplicated summary: `reports/final-defect-summary/Final_Defect_Summary_Chethan_Poojary.xlsx`

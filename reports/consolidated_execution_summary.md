# Consolidated Execution Summary

- Total sheets processed: 10
- Total UI test cases: 45
- Total API test cases: 69
- Total passed: 52
- Total failed: 62
- Total skipped: 0
- Coverage percentage: 100.0%

## Per-Sheet Results

| Sheet | Cases | UI | API | Passed | Failed | Skipped |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1_HappyPath | 8 | 4 | 8 | 3 | 9 | 0 |
| 2_Lifecycle | 7 | 6 | 7 | 5 | 8 | 0 |
| 3_RoleBoundary | 7 | 4 | 7 | 6 | 5 | 0 |
| 4_RegionBoundary | 6 | 2 | 6 | 1 | 7 | 0 |
| 5_Citation | 7 | 3 | 7 | 0 | 10 | 0 |
| 6_Hallucination | 7 | 4 | 7 | 7 | 4 | 0 |
| 7_Security | 8 | 7 | 8 | 7 | 8 | 0 |
| 8_EdgeCases | 8 | 7 | 8 | 4 | 11 | 0 |
| 9_CrossRegion | 5 | 5 | 5 | 10 | 0 | 0 |
| 10_APIvsUI | 6 | 3 | 6 | 9 | 0 | 0 |

## Gaps, Ambiguities, Duplicates, Missing Edge Cases

- **Medium Specification gap** (9_CrossRegion / TC-CR-001): Expected behavior asks to document actual behavior rather than assert a product rule.
- **Medium Specification gap** (9_CrossRegion / TC-CR-002): Expected behavior asks to document actual behavior rather than assert a product rule.
- **Medium Specification gap** (9_CrossRegion / TC-CR-003): Expected behavior asks to document actual behavior rather than assert a product rule.
- **Medium Specification gap** (9_CrossRegion / TC-CR-004): Expected behavior asks to document actual behavior rather than assert a product rule.
- **Medium Specification gap** (9_CrossRegion / TC-CR-005): Expected behavior asks to document actual behavior rather than assert a product rule.

## Recommendations

- Clarify cross-region home-region versus destination-region policy behavior.
- Define exact refusal wording expectations to reduce brittle assertion logic.
- Add stable data-testid attributes to UI controls for robust automation.
- Document the expected API schema for citations and document filtering.
- Separate exploratory/spec-gap rows from release-gating regression rows.

## Assumptions, Risks, Blockers

- UI automation uses resilient label/role-based selectors because no stable data-testid contract is available.
- Spec-gap scenarios are treated as service stability checks and documented behavior rather than strict pass/fail business assertions.
- Live service defects are reported as failed tests and preserved in Allure evidence.
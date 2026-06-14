# Risk Assessment - Knowledge Assistant

## Business Risks

| Risk | Impact |
| --- | --- |
| Employees receive incorrect policy information | High |
| Retired or draft policies influence decisions | High |
| Restricted information exposed to unauthorized users | High |

## Technical Risks

| Risk | Impact |
| --- | --- |
| Incorrect citation mapping | High |
| Region or role filtering logic defects | High |
| UI document panel inconsistent with API | Medium |

## GenAI Risks

| Risk | Impact |
| --- | --- |
| Hallucinated answers | High |
| Prompt injection bypass | High |
| Unsupported claims presented as facts | High |

## Mitigations

- Golden-question regression suite
- Data-driven authorization tests
- Citation validation against the content library
- Adversarial prompt testing


# Reflection

Testing this Knowledge Assistant is different from testing a deterministic form or CRUD workflow. The most important failures are semantic: the assistant may return a plausible but unsupported answer, cite the wrong document, use retired or draft content, or reveal content outside the user's region or role. For that reason, the test approach must focus on product rules and evidence rather than exact answer text.

## Where AI/LLM Evaluation Helps

AI evaluation tools such as RAGAS are useful for measuring qualities that traditional assertions do not capture well:

- whether the answer is grounded in retrieved context;
- whether the answer is relevant to the question;
- whether retrieval brought back useful supporting context;
- whether the generated answer is faithful to the source material;
- whether answers drift over time after a model, prompt, or index change.

These metrics are useful as a trend and monitoring signal, especially for real RAG systems where responses may vary across model versions. They help identify weak retrieval, poor grounding, and hallucination risk at scale.

## Where AI/LLM Evaluation Falls Short

RAGAS and similar tools should not replace deterministic business-rule checks. For this assignment, some rules are exact and must be asserted directly:

- APAC In Review policy `D-003` must not be treated as approved.
- Retired policy `D-005` must not be surfaced as current guidance.
- Finance-only document `D-008` must not be exposed to unauthorized roles.
- Americas users should not receive EMEA travel allowance values.
- A citation must point to the correct approved document.

Judge-based metrics can also be expensive, slow, quota-dependent, and occasionally inconsistent. They are best used as an additional evaluation layer, not the source of truth for access control, lifecycle, or citation correctness.

## Checks That Should Survive a Model Swap

The most durable checks are rule-based and source-grounded:

- required and forbidden document IDs;
- required policy values such as `USD 75`, `EUR 60`, `3 days`, `CFO`, or `4%`;
- refusal behavior when approved authorized content is unavailable;
- lifecycle exclusion for Draft, In Review, and Retired documents;
- role and region scoping;
- documents panel visibility;
- API status and response structure.

These should survive a model swap because they assert business requirements rather than exact wording.

## Checks That May Be Brittle

Exact phrasing, full response text, sentence order, and style-based checks are more likely to break after a prompt or model change. For that reason, the automation avoids exact full-string matching and focuses on durable evidence.

Some UI checks can also be brittle if selectors or layout change. The suite uses a Page Object Model to isolate UI interaction logic and make future selector updates easier.

## Use of AI Coding Assistance

AI assistance is helpful for scaffolding tests, generating reusable code, and speeding up report creation, but the resulting code still needs human review. My approach was to keep the suite maintainable by:

- driving tests from a golden-question dataset;
- avoiding copy-pasted near-duplicate tests;
- separating API, UI, framework, reporting, and evaluation code;
- keeping assertions tied to product rules;
- preserving raw request/response evidence and screenshots;
- validating generated reports after execution.

The main do's and don'ts:

- Do use AI to accelerate boilerplate and reporting.
- Do review assertions carefully against the product spec and content library.
- Do keep test data explicit and auditable.
- Do not blindly trust generated tests without executing them.
- Do not use exact generated wording as the only validation.
- Do not hide known gaps or product failures.

## What I Would Add With More Time

With more time, I would add:

- scheduled CI execution with historical trend reports;
- load and concurrency testing for `/query` and `/documents`;
- browser compatibility coverage;
- drift monitoring across model/prompt/index changes;
- richer RAGAS or DeepEval baselines once evaluator API quota is available;
- severity triage workflow integrated with GitHub issues;
- a small dashboard showing pass rate, defect trend, and high-risk failure areas over time.

Overall, the strongest confidence comes from combining deterministic rule-based tests with AI evaluation signals. The deterministic suite protects access, lifecycle, citation, and compliance rules; the AI evaluation layer helps monitor broader answer quality and grounding.

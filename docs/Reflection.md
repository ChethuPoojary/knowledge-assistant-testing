# Reflection - GenAI Testing

## Where AI Evaluation Helps

- Automated grounding checks
- Semantic similarity evaluation
- Large-scale regression scoring
- Detecting answer drift after model changes

## Where AI Evaluation Falls Short

- Evaluators can hallucinate their own judgments.
- Subtle authorization leaks may be missed.
- Business-critical wording differences require human review.
- Safety and compliance requirements often need deterministic assertions.

## Checks Most Likely to Survive a Model Swap

- Authorization rules
- Lifecycle filtering
- Citation presence
- Refusal for out-of-scope questions

## Checks Likely to Need Adjustment

- Exact wording assertions
- Response formatting
- Ranking of multiple valid citations

## Lessons Learned

### Golden datasets are essential

A curated set of questions and expected outcomes provides stable regression coverage.

### API-first testing reduces brittleness

Most policy and access rules can be validated more reliably through the API than the UI.

### GenAI systems require layered validation

Functional correctness, grounding, citations, safety, and authorization must all be tested independently.

## Future Improvements

- Add Ragas or DeepEval scoring for grounding and hallucination detection.
- Add continuous monitoring for answer drift.
- Expand adversarial prompt coverage.
- Integrate accessibility testing into CI.


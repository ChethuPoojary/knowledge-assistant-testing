from __future__ import annotations

import re
from collections import Counter
from typing import Any

try:
    import tiktoken
except Exception:  # pragma: no cover
    tiktoken = None


def estimate_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    if not text:
        return 0
    if tiktoken is None:
        return max(1, len(text.split()))
    try:
        encoding = tiktoken.encoding_for_model(model)
    except Exception:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def keyword_overlap_score(expected: str, actual: str) -> float:
    expected_terms = _important_terms(expected)
    if not expected_terms:
        return 0.0
    actual_lower = (actual or "").lower()
    matched = sum(1 for term in expected_terms if term.lower() in actual_lower)
    return round(matched / len(expected_terms), 4)


def retrieval_success_rate(contexts: list[str], citations: list[str]) -> float:
    return 1.0 if contexts or citations else 0.0


def context_utilization_score(answer: str, contexts: list[str]) -> float:
    if not answer or not contexts:
        return 0.0
    answer_terms = _token_counter(answer)
    context_terms = _token_counter(" ".join(contexts))
    if not answer_terms:
        return 0.0
    used = sum(count for term, count in answer_terms.items() if term in context_terms)
    total = sum(answer_terms.values())
    return round(used / total, 4)


def hallucination_flag(answer: str, contexts: list[str], expected: str) -> int:
    if not answer:
        return 0
    if not contexts:
        refusal_terms = ("do not have", "cannot", "unable", "not available", "no approved")
        return 0 if any(term in answer.lower() for term in refusal_terms) else 1
    utilization = context_utilization_score(answer, contexts)
    overlap = keyword_overlap_score(expected, answer)
    return 1 if utilization < 0.2 and overlap < 0.3 else 0


def cost_estimate(input_tokens: int, output_tokens: int, input_per_1k: float, output_per_1k: float) -> float:
    return round((input_tokens / 1000 * input_per_1k) + (output_tokens / 1000 * output_per_1k), 6)


def custom_metric_row(result: Any, evaluator_model: str, input_cost: float, output_cost: float) -> dict:
    input_tokens = estimate_tokens(result.question + "\n" + "\n".join(result.contexts), evaluator_model)
    output_tokens = estimate_tokens(result.answer, evaluator_model)
    return {
        "latency_ms": round(result.latency_ms, 2),
        "response_time_seconds": round(result.latency_ms / 1000, 3),
        "status_code": result.status_code,
        "input_tokens_estimated": input_tokens,
        "output_tokens_estimated": output_tokens,
        "total_tokens_estimated": input_tokens + output_tokens,
        "cost_estimated": cost_estimate(input_tokens, output_tokens, input_cost, output_cost),
        "retrieval_success_rate": retrieval_success_rate(result.contexts, result.citations),
        "context_utilization_custom": context_utilization_score(result.answer, result.contexts),
        "response_accuracy_custom": keyword_overlap_score(result.expected_answer, result.answer),
        "hallucination_detected_custom": hallucination_flag(result.answer, result.contexts, result.expected_answer),
    }


def _important_terms(text: str) -> list[str]:
    patterns = [
        r"\bD-\d{3}\b",
        r"\b(?:USD|EUR|JPY)\s?\d[\d,]*\b",
        r"\b\d+\s*days?\b",
        r"\b\d+%\b",
        r"\bCFO\b",
        r"\bVP\b",
        r"\bQ[1-4]\b",
    ]
    terms = []
    for pattern in patterns:
        terms.extend(match.group(0) for match in re.finditer(pattern, text or "", re.I))
    if not terms:
        terms = [word for word in re.findall(r"\b[A-Za-z]{5,}\b", text or "")[:8]]
    return list(dict.fromkeys(terms))


def _token_counter(text: str) -> Counter:
    terms = re.findall(r"\b[a-zA-Z0-9]{3,}\b", (text or "").lower())
    stopwords = {"the", "and", "for", "you", "with", "that", "this", "are", "from", "have", "not"}
    return Counter(term for term in terms if term not in stopwords)

from __future__ import annotations

import importlib
import json
import os
from dataclasses import asdict
from pathlib import Path
from typing import Any

import pandas as pd

from framework.models import TestCase
from rag_evaluation.app_adapter import RagAppResult


RAGAS_METRIC_IMPORTS = {
    "context_precision": [
        ("ragas.metrics", "LLMContextPrecisionWithoutReference"),
        ("ragas.metrics", "context_precision"),
    ],
    "context_recall": [
        ("ragas.metrics", "LLMContextRecall"),
        ("ragas.metrics", "context_recall"),
    ],
    "context_entities_recall": [
        ("ragas.metrics", "ContextEntityRecall"),
        ("ragas.metrics", "context_entity_recall"),
    ],
    "noise_sensitivity": [
        ("ragas.metrics", "NoiseSensitivity"),
        ("ragas.metrics", "noise_sensitivity"),
    ],
    "response_relevancy": [
        ("ragas.metrics", "ResponseRelevancy"),
        ("ragas.metrics", "answer_relevancy"),
    ],
    "faithfulness": [
        ("ragas.metrics", "Faithfulness"),
        ("ragas.metrics", "faithfulness"),
    ],
    "answer_correctness": [
        ("ragas.metrics", "AnswerCorrectness"),
        ("ragas.metrics", "answer_correctness"),
    ],
    "semantic_similarity": [
        ("ragas.metrics", "SemanticSimilarity"),
        ("ragas.metrics", "answer_similarity"),
    ],
    "factual_correctness": [
        ("ragas.metrics", "FactualCorrectness"),
    ],
    "answer_accuracy": [
        ("ragas.metrics", "AnswerAccuracy"),
    ],
    "context_relevance": [
        ("ragas.metrics", "ContextRelevance"),
    ],
    "response_groundedness": [
        ("ragas.metrics", "ResponseGroundedness"),
    ],
}


def build_ragas_dataframe(results: list[RagAppResult]) -> pd.DataFrame:
    rows = []
    for result in results:
        rows.append(
            {
                "user_input": result.question,
                "question": result.question,
                "response": result.answer,
                "answer": result.answer,
                "retrieved_contexts": result.contexts,
                "contexts": result.contexts,
                "reference": result.expected_answer,
                "ground_truth": result.expected_answer,
                "reference_contexts": result.contexts,
                "test_case_id": result.test_case_id,
                "sheet": result.sheet,
                "category": result.category,
                "region": result.region,
                "role": result.role,
            }
        )
    return pd.DataFrame(rows)


def run_ragas_metrics(results: list[RagAppResult], output_dir: Path, enabled: bool = True) -> tuple[pd.DataFrame, dict]:
    metadata: dict[str, Any] = {"enabled": enabled, "metrics_requested": list(RAGAS_METRIC_IMPORTS)}
    if not enabled:
        metadata["skip_reason"] = "RAGAS metrics disabled by configuration."
        return pd.DataFrame(), metadata
    if not (os.getenv("OPENAI_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")):
        metadata["skip_reason"] = "No evaluator LLM API key found. Set OPENAI_API_KEY or AZURE_OPENAI_API_KEY."
        return pd.DataFrame(), metadata

    try:
        ragas_module = importlib.import_module("ragas")
        evaluate = getattr(ragas_module, "evaluate")
    except Exception as exc:
        metadata["skip_reason"] = f"RAGAS is not installed/importable: {exc!r}"
        return pd.DataFrame(), metadata

    metrics, unavailable = _load_metrics()
    metadata["metrics_loaded"] = [_metric_name(metric) for metric in metrics]
    metadata["metrics_unavailable"] = unavailable
    if not metrics:
        metadata["skip_reason"] = "No compatible RAGAS metrics could be imported for the installed version."
        return pd.DataFrame(), metadata

    dataframe = build_ragas_dataframe(results)
    output_dir.mkdir(parents=True, exist_ok=True)
    dataframe.to_json(output_dir / "ragas_dataset.jsonl", orient="records", lines=True)

    try:
        try:
            from datasets import Dataset

            dataset = Dataset.from_pandas(dataframe)
            ragas_result = evaluate(dataset=dataset, metrics=metrics)
        except TypeError:
            ragas_result = evaluate(dataframe, metrics=metrics)

        ragas_scores = _result_to_dataframe(ragas_result)
        identity = dataframe[["test_case_id", "sheet", "category", "region", "role"]].reset_index(drop=True)
        ragas_scores = pd.concat([identity, ragas_scores.reset_index(drop=True)], axis=1)
        return ragas_scores, metadata
    except Exception as exc:
        metadata["error"] = repr(exc)
        return pd.DataFrame(), metadata


def _load_metrics() -> tuple[list[Any], dict[str, str]]:
    metrics = []
    unavailable = {}
    for metric_name, candidates in RAGAS_METRIC_IMPORTS.items():
        loaded = None
        last_error = ""
        for module_name, attr_name in candidates:
            try:
                module = importlib.import_module(module_name)
                metric_obj = getattr(module, attr_name)
                loaded = metric_obj() if isinstance(metric_obj, type) else metric_obj
                break
            except Exception as exc:
                last_error = repr(exc)
        if loaded is None:
            unavailable[metric_name] = last_error or "not found"
        else:
            metrics.append(loaded)
    return metrics, unavailable


def _metric_name(metric: Any) -> str:
    return getattr(metric, "name", None) or metric.__class__.__name__


def _result_to_dataframe(ragas_result: Any) -> pd.DataFrame:
    if hasattr(ragas_result, "to_pandas"):
        return ragas_result.to_pandas()
    if hasattr(ragas_result, "to_dataframe"):
        return ragas_result.to_dataframe()
    if isinstance(ragas_result, pd.DataFrame):
        return ragas_result
    if isinstance(ragas_result, dict):
        return pd.DataFrame(ragas_result)
    return pd.DataFrame(json.loads(json.dumps(ragas_result, default=str)))


def results_to_dataframe(results: list[RagAppResult]) -> pd.DataFrame:
    rows = []
    for result in results:
        row = asdict(result)
        row["contexts"] = json.dumps(result.contexts, ensure_ascii=False)
        row["citations"] = json.dumps(result.citations, ensure_ascii=False)
        row["request_payload"] = json.dumps(result.request_payload, ensure_ascii=False)
        row["response_payload"] = json.dumps(result.response_payload, ensure_ascii=False)
        rows.append(row)
    return pd.DataFrame(rows)

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from framework.testsuite_loader import load_cases
from rag_evaluation.app_adapter import KnowledgeAssistantRagAdapter
from rag_evaluation.config import RagasEvaluationConfig
from rag_evaluation.custom_metrics import custom_metric_row
from rag_evaluation.ragas_runner import results_to_dataframe, run_ragas_metrics
from rag_evaluation.reporting import write_reports


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run RAGAS evaluation for the Knowledge Assistant RAG application.")
    parser.add_argument("--output-dir", default=None, help="Output directory for evaluation reports.")
    parser.add_argument("--max-cases", type=int, default=None, help="Limit number of cases for smoke runs.")
    parser.add_argument("--layers", default="API,Both", help="Comma-separated Testing Layer values to evaluate.")
    parser.add_argument("--skip-ragas", action="store_true", help="Only run custom metrics; skip RAGAS judge metrics.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = RagasEvaluationConfig()
    if args.output_dir:
        config.output_dir = Path(args.output_dir)
    if args.max_cases:
        config.max_cases = args.max_cases
    if args.layers:
        config.include_layers = {item.strip() for item in args.layers.split(",") if item.strip()}
    if args.skip_ragas:
        config.run_ragas_metrics = False

    cases = [
        case
        for case in load_cases(config.test_suite_file)
        if case.testing_layer in config.include_layers and not case.is_spec_gap
    ]
    if config.max_cases:
        cases = cases[: config.max_cases]

    config.output_dir.mkdir(parents=True, exist_ok=True)
    adapter = KnowledgeAssistantRagAdapter(config.base_url, config.timeout_seconds)

    results = []
    custom_rows = []
    for index, case in enumerate(cases, start=1):
        print(f"[{index}/{len(cases)}] Evaluating {case.sheet}::{case.test_case_id}")
        result = adapter.evaluate_case(case)
        results.append(result)
        custom_rows.append(
            {
                "test_case_id": result.test_case_id,
                "sheet": result.sheet,
                "category": result.category,
                "region": result.region,
                "role": result.role,
                "question": result.question,
                "answer": result.answer,
                "expected_answer": result.expected_answer,
                **custom_metric_row(
                    result,
                    config.evaluator_model,
                    config.currency_per_1k_input_tokens,
                    config.currency_per_1k_output_tokens,
                ),
            }
        )

    raw_df = results_to_dataframe(results)
    custom_df = pd.DataFrame(custom_rows)
    ragas_df, ragas_metadata = run_ragas_metrics(
        results,
        config.output_dir,
        enabled=config.run_ragas_metrics and config.has_evaluator_key,
    )
    if config.run_ragas_metrics and not config.has_evaluator_key:
        ragas_metadata["skip_reason"] = "Set OPENAI_API_KEY to enable RAGAS LLM/embedding judge metrics."

    write_reports(config.output_dir, raw_df, custom_df, ragas_df, ragas_metadata)
    print("")
    print(f"RAG evaluation complete: {config.output_dir}")
    print(f"Open report: {config.output_dir / 'index.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

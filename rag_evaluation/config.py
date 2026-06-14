from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from framework.config import BASE_URL, REPORTS_DIR, TEST_SUITE_FILE


@dataclass
class RagasEvaluationConfig:
    base_url: str = os.getenv("RAG_APP_BASE_URL", BASE_URL)
    test_suite_file: Path = Path(os.getenv("RAG_TEST_SUITE_FILE", str(TEST_SUITE_FILE)))
    output_dir: Path = Path(os.getenv("RAG_EVAL_OUTPUT_DIR", str(REPORTS_DIR / "ragas-evaluation")))
    timeout_seconds: int = int(os.getenv("RAG_EVAL_TIMEOUT_SECONDS", "30"))
    max_cases: int | None = int(os.getenv("RAG_EVAL_MAX_CASES", "0")) or None
    include_layers: set[str] = field(default_factory=lambda: {"API", "Both"})
    evaluator_model: str = os.getenv("RAGAS_EVALUATOR_MODEL", "gpt-4o-mini")
    embedding_model: str = os.getenv("RAGAS_EMBEDDING_MODEL", "text-embedding-3-small")
    currency_per_1k_input_tokens: float = float(os.getenv("RAG_EVAL_INPUT_COST_PER_1K", "0"))
    currency_per_1k_output_tokens: float = float(os.getenv("RAG_EVAL_OUTPUT_COST_PER_1K", "0"))
    run_ragas_metrics: bool = os.getenv("RAGAS_RUN_METRICS", "auto").lower() in {"1", "true", "yes", "auto"}

    @property
    def has_evaluator_key(self) -> bool:
        return bool(os.getenv("OPENAI_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY"))

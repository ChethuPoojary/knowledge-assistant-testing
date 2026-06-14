from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def write_reports(
    output_dir: Path,
    raw_df: pd.DataFrame,
    custom_df: pd.DataFrame,
    ragas_df: pd.DataFrame,
    ragas_metadata: dict,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_df.to_csv(output_dir / "raw_app_responses.csv", index=False)
    custom_df.to_csv(output_dir / "custom_metrics.csv", index=False)
    if not ragas_df.empty:
        ragas_df.to_csv(output_dir / "ragas_metrics.csv", index=False)

    merged = custom_df.copy()
    if not ragas_df.empty:
        merge_cols = ["test_case_id", "sheet", "category", "region", "role"]
        merged = merged.merge(ragas_df, on=merge_cols, how="left", suffixes=("", "_ragas"))
    merged.to_csv(output_dir / "rag_evaluation_results.csv", index=False)

    summary = build_summary(merged, ragas_metadata)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    (output_dir / "summary.md").write_text(render_markdown_summary(summary), encoding="utf-8")
    render_charts(output_dir, merged)
    render_html_report(output_dir, summary, merged)


def build_summary(results: pd.DataFrame, ragas_metadata: dict) -> dict:
    numeric = results.select_dtypes(include="number")
    metric_means = numeric.mean(numeric_only=True).round(4).to_dict()
    by_sheet = (
        results.groupby("sheet")
        .agg(
            cases=("test_case_id", "count"),
            avg_latency_ms=("latency_ms", "mean"),
            retrieval_success_rate=("retrieval_success_rate", "mean"),
            response_accuracy_custom=("response_accuracy_custom", "mean"),
            hallucination_rate=("hallucination_detected_custom", "mean"),
        )
        .round(4)
        .reset_index()
        .to_dict(orient="records")
        if not results.empty
        else []
    )
    return {
        "total_cases": int(len(results)),
        "metric_means": metric_means,
        "by_sheet": by_sheet,
        "ragas": ragas_metadata,
    }


def render_markdown_summary(summary: dict) -> str:
    lines = [
        "# RAG Evaluation Summary",
        "",
        f"Total cases evaluated: {summary['total_cases']}",
        "",
        "## Metric Means",
    ]
    for key, value in summary["metric_means"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Sheet Summary"])
    for row in summary["by_sheet"]:
        lines.append(
            f"- {row['sheet']}: cases={row['cases']}, avg_latency_ms={row['avg_latency_ms']}, "
            f"retrieval_success_rate={row['retrieval_success_rate']}, hallucination_rate={row['hallucination_rate']}"
        )
    if summary["ragas"].get("skip_reason"):
        lines.extend(["", "## RAGAS Metrics", f"Skipped: {summary['ragas']['skip_reason']}"])
    return "\n".join(lines) + "\n"


def render_charts(output_dir: Path, results: pd.DataFrame) -> None:
    charts_dir = output_dir / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)
    if results.empty:
        return

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 5))
    sns.barplot(data=results, x="sheet", y="latency_ms", errorbar=None)
    plt.xticks(rotation=35, ha="right")
    plt.title("Average Response Latency by Sheet")
    plt.tight_layout()
    plt.savefig(charts_dir / "latency_by_sheet.png", dpi=150)
    plt.close()

    plt.figure(figsize=(10, 5))
    sheet_metrics = results.groupby("sheet")[["retrieval_success_rate", "response_accuracy_custom", "context_utilization_custom"]].mean()
    sns.heatmap(sheet_metrics, annot=True, cmap="YlGnBu", vmin=0, vmax=1)
    plt.title("Custom RAG Metric Heatmap")
    plt.tight_layout()
    plt.savefig(charts_dir / "custom_metric_heatmap.png", dpi=150)
    plt.close()

    if "hallucination_detected_custom" in results:
        plt.figure(figsize=(8, 4))
        hallucination = results.groupby("sheet")["hallucination_detected_custom"].mean().reset_index()
        sns.barplot(data=hallucination, x="sheet", y="hallucination_detected_custom", errorbar=None)
        plt.xticks(rotation=35, ha="right")
        plt.title("Hallucination Detection Rate by Sheet")
        plt.tight_layout()
        plt.savefig(charts_dir / "hallucination_rate_by_sheet.png", dpi=150)
        plt.close()


def render_html_report(output_dir: Path, summary: dict, results: pd.DataFrame) -> None:
    table_html = results.head(200).to_html(index=False, escape=True)
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>RAG Evaluation Report</title>
  <style>
    body {{ font-family: Segoe UI, Arial, sans-serif; margin: 24px; color: #172033; }}
    h1, h2 {{ color: #1f4e79; }}
    .tile {{ display: inline-block; border: 1px solid #d9e2f3; border-radius: 8px; padding: 12px 16px; margin: 8px; }}
    .tile strong {{ display: block; font-size: 24px; }}
    img {{ max-width: 900px; border: 1px solid #d9e2f3; border-radius: 6px; margin: 12px 0; }}
    table {{ border-collapse: collapse; width: 100%; font-size: 12px; }}
    th, td {{ border: 1px solid #d9e2f3; padding: 6px; vertical-align: top; }}
    th {{ background: #1f4e79; color: white; }}
  </style>
</head>
<body>
  <h1>RAG Evaluation Report</h1>
  <div class="tile"><strong>{summary['total_cases']}</strong>Cases Evaluated</div>
  <h2>Charts</h2>
  <img src="charts/latency_by_sheet.png" alt="Latency by sheet">
  <img src="charts/custom_metric_heatmap.png" alt="Custom metric heatmap">
  <img src="charts/hallucination_rate_by_sheet.png" alt="Hallucination rate">
  <h2>Metric Means</h2>
  <pre>{json.dumps(summary['metric_means'], indent=2)}</pre>
  <h2>RAGAS Status</h2>
  <pre>{json.dumps(summary['ragas'], indent=2)}</pre>
  <h2>Results Preview</h2>
  {table_html}
</body>
</html>"""
    (output_dir / "index.html").write_text(html, encoding="utf-8")

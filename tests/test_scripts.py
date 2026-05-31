from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "engineering-thesis-zh" / "scripts"


def run_script(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )


def test_markdown_outline_and_corpus_analysis(tmp_path: Path) -> None:
    draft = tmp_path / "draft.md"
    draft.write_text(
        "\n".join(
            [
                "# 数字孪生驱动的维护优化研究",
                "## 摘要",
                "关键词：数字孪生；维护策略；生产调度",
                "# 第1章 绪论",
                "## 1.1 研究背景",
                "# 第2章 理论基础",
                "## 2.1 离散事件仿真",
                "# 第3章 问题建模",
                "# 第4章 实验分析",
                "图 4-1 策略对比图",
                "表 4-1 实验参数表",
                "# 第5章 总结",
            ]
        ),
        encoding="utf-8",
    )
    records = tmp_path / "records.jsonl"
    stats_dir = tmp_path / "stats"

    run_script(str(SCRIPTS / "extract_markdown_outline.py"), str(draft), "--output", str(records))
    run_script(str(SCRIPTS / "quality_check.py"), str(records), "--min-headings", "5")
    run_script(str(SCRIPTS / "analyze_corpus.py"), str(records), "--output-dir", str(stats_dir))

    record = json.loads(records.read_text(encoding="utf-8").strip())
    assert record["keyword_candidates"] == ["数字孪生", "维护策略", "生产调度"]
    assert "第4章 实验分析" in record["headings"]
    assert "图 4-1 策略对比图" in record["figure_table_titles"]

    summary = json.loads((stats_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["record_count"] == 1
    assert summary["parse_error_count"] == 0


def test_manifest_and_empty_pipeline(tmp_path: Path) -> None:
    corpus = tmp_path / "private_corpus"
    (corpus / "software").mkdir(parents=True)
    (corpus / "software" / "2024_school_system.pdf").write_bytes(b"%PDF synthetic placeholder")
    manifest = tmp_path / "manifest.csv"

    run_script(str(SCRIPTS / "build_manifest.py"), str(corpus), "--output", str(manifest))

    manifest_text = manifest.read_text(encoding="utf-8-sig")
    assert "2024_school_system.pdf" in manifest_text
    assert "software" in manifest_text

    empty_corpus = tmp_path / "empty"
    empty_corpus.mkdir()
    private_dir = tmp_path / "private_extracts"
    public_dir = tmp_path / "public_stats"
    result = run_script(
        str(SCRIPTS / "run_corpus_pipeline.py"),
        "--corpus-root",
        str(empty_corpus),
        "--private-dir",
        str(private_dir),
        "--public-dir",
        str(public_dir),
        "--allow-empty",
    )
    assert "No PDFs found; manifest smoke test completed." in result.stdout
    assert (private_dir / "manifest.csv").exists()


def test_experiment_metric_summary_handles_ties(tmp_path: Path) -> None:
    csv_dir = tmp_path / "csv"
    csv_dir.mkdir()
    (csv_dir / "maintenance_compare.csv").write_text(
        "\n".join(
            [
                "maintenance_policy,makespan,on_time_rate,maintenance_cost",
                "CM_ONLY,21,1,0",
                "AGE,21,1,0",
            ]
        ),
        encoding="utf-8",
    )
    output = tmp_path / "summary.md"

    run_script(str(SCRIPTS / "summarize_experiment_metrics.py"), str(csv_dir), "--output", str(output))

    text = output.read_text(encoding="utf-8")
    assert "all compared rows have the same makespan" in text
    assert "do not claim a difference" in text


def test_public_safety_fails_on_public_pdf(tmp_path: Path) -> None:
    public_pdf = tmp_path / "leaked.pdf"
    public_pdf.write_bytes(b"%PDF synthetic placeholder")

    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "check_public_safety.py"), str(tmp_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1
    assert "banned document file" in result.stdout


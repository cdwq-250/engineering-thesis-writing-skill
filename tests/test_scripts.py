from __future__ import annotations

import json
import os
import subprocess
import sys
import time
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
    run_script(
        str(SCRIPTS / "write_corpus_report.py"),
        "--stats-dir",
        str(stats_dir),
        "--records",
        str(records),
        "--output",
        str(stats_dir / "progress_report.md"),
    )
    run_script(
        str(SCRIPTS / "write_acquisition_plan.py"),
        "--summary",
        str(stats_dir / "summary.json"),
        "--output-md",
        str(stats_dir / "acquisition_plan.md"),
        "--output-csv",
        str(stats_dir / "acquisition_plan.csv"),
        "--target-per-family",
        "3",
        "--batch-size",
        "2",
    )

    record = json.loads(records.read_text(encoding="utf-8").strip())
    assert record["keyword_candidates"] == ["数字孪生", "维护策略", "生产调度"]
    assert "第4章 实验分析" in record["headings"]
    assert "图 4-1 策略对比图" in record["figure_table_titles"]

    summary = json.loads((stats_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["record_count"] == 1
    assert summary["parse_error_count"] == 0
    report = (stats_dir / "progress_report.md").read_text(encoding="utf-8")
    assert "Records analyzed: 1" in report
    assert "Next Acquisition Batch" in report
    plan = (stats_dir / "acquisition_plan.md").read_text(encoding="utf-8")
    assert "Next Search Tasks" in plan
    assert "software" in plan
    assert "mechanical/manufacturing" in plan


def test_manifest_and_empty_pipeline(tmp_path: Path) -> None:
    corpus = tmp_path / "private_corpus"
    (corpus / "software").mkdir(parents=True)
    (corpus / "software" / "2024_school_system.pdf").write_bytes(b"%PDF synthetic placeholder")
    (corpus / "software" / "2024_school_system.caj").write_bytes(b"CAJ synthetic placeholder")
    (corpus / "software" / "2024_school_system.nh").write_bytes(b"NH synthetic placeholder")
    manifest = tmp_path / "manifest.csv"

    run_script(str(SCRIPTS / "build_manifest.py"), str(corpus), "--output", str(manifest))

    manifest_text = manifest.read_text(encoding="utf-8-sig")
    assert "2024_school_system.pdf" in manifest_text
    assert "2024_school_system.caj" in manifest_text
    assert "2024_school_system.nh" in manifest_text
    assert "software" in manifest_text
    assert "ready_for_extraction" in manifest_text
    assert "convert_to_pdf_first" in manifest_text

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


def test_archive_downloads_copies_supported_files_and_skips_duplicates(tmp_path: Path) -> None:
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    destination = tmp_path / "private_corpus" / "cnki_manual"
    (downloads / "paper.pdf").write_bytes(b"%PDF paper")
    (downloads / "paper-copy.pdf").write_bytes(b"%PDF paper")
    (downloads / "paper.caj").write_bytes(b"CAJ paper")
    (downloads / "ignore.txt").write_text("not a thesis file", encoding="utf-8")

    result = run_script(
        str(SCRIPTS / "archive_downloads.py"),
        "--source",
        str(downloads),
        "--destination",
        str(destination),
    )

    assert "copied=2" in result.stdout
    assert "duplicates=1" in result.stdout
    assert len(list(destination.glob("*.pdf"))) == 1
    assert (destination / "paper.caj").exists()
    assert not (destination / "ignore.txt").exists()


def test_archive_downloads_filters_by_name_type_and_age(tmp_path: Path) -> None:
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    destination = tmp_path / "private_corpus" / "cnki_manual"
    target = downloads / "设备维护优化研究.pdf"
    excluded = downloads / "选题报告.doc"
    non_pdf = downloads / "设备维护优化研究.caj"
    old = downloads / "旧论文维护研究.pdf"
    target.write_bytes(b"%PDF target")
    excluded.write_bytes(b"DOC report")
    non_pdf.write_bytes(b"CAJ target")
    old.write_bytes(b"%PDF old")
    old_time = time.time() - 60 * 60 * 24 * 30
    os.utime(old, (old_time, old_time))

    result = run_script(
        str(SCRIPTS / "archive_downloads.py"),
        "--source",
        str(downloads),
        "--destination",
        str(destination),
        "--include",
        "维护|优化",
        "--exclude",
        "选题|报告",
        "--pdf-only",
        "--since-days",
        "7",
    )

    assert "copied=1" in result.stdout
    assert "skip:not_pdf" in result.stdout
    assert "skip:older_than_since" in result.stdout
    assert (destination / "设备维护优化研究.pdf").exists()
    assert not (destination / "选题报告.doc").exists()
    assert not (destination / "设备维护优化研究.caj").exists()
    assert not (destination / "旧论文维护研究.pdf").exists()


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


def test_skill_references_have_readable_chinese() -> None:
    expected = {
        "software-system-thesis.md": "详细设计与实现",
        "control-optimization-thesis.md": "问题建模",
        "mechanical-manufacturing-thesis.md": "设备状态",
    }
    for file_name, phrase in expected.items():
        text = (ROOT / "engineering-thesis-zh" / "references" / file_name).read_text(encoding="utf-8")
        assert phrase in text

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
        str(SCRIPTS / "analyze_commonalities.py"),
        str(records),
        "--output-md",
        str(stats_dir / "common_patterns.md"),
        "--output-csv",
        str(stats_dir / "commonality_matrix.csv"),
        "--min-support",
        "1",
    )
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
    run_script(
        str(SCRIPTS / "write_rule_candidates.py"),
        "--stats-dir",
        str(stats_dir),
        "--output",
        str(stats_dir / "rule_candidates.md"),
    )
    run_script(
        str(SCRIPTS / "check_corpus_readiness.py"),
        "--summary",
        str(stats_dir / "summary.json"),
        "--output",
        str(stats_dir / "readiness_report.md"),
        "--min-total-records",
        "3",
        "--target-per-family",
        "3",
    )

    record = json.loads(records.read_text(encoding="utf-8").strip())
    assert record["keyword_candidates"] == ["数字孪生", "维护策略", "生产调度"]
    assert "第4章 实验分析" in record["headings"]
    assert "图 4-1 策略对比图" in record["figure_table_titles"]

    summary = json.loads((stats_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["record_count"] == 1
    assert summary["parse_error_count"] == 0
    assert "classification_confidence_counts" in summary
    assert (stats_dir / "classification_diagnostics.csv").exists()
    assert (stats_dir / "topic_tags.csv").exists()
    assert (stats_dir / "topic_cooccurrence.csv").exists()
    role_signal_text = (stats_dir / "chapter_role_signals.csv").read_text(encoding="utf-8")
    assert "role,count" in role_signal_text
    report = (stats_dir / "progress_report.md").read_text(encoding="utf-8")
    assert "Records analyzed: 1" in report
    assert "Classification Confidence" in report
    assert "Topic Co-Occurrence" in report
    assert "Chapter Role Signals" in report
    assert "Next Acquisition Batch" in report
    common_patterns = (stats_dir / "common_patterns.md").read_text(encoding="utf-8")
    assert "Common Patterns Report" in common_patterns
    assert "Evidence Boundary" in common_patterns
    assert (stats_dir / "commonality_matrix.csv").exists()
    plan = (stats_dir / "acquisition_plan.md").read_text(encoding="utf-8")
    assert "Next Search Tasks" in plan
    assert "software" in plan
    assert "mechanical/manufacturing" in plan
    assert "Batch Policy" in plan
    assert "Coverage Milestones" in plan
    assert "Acceptance Filters" in plan
    plan_csv = (stats_dir / "acquisition_plan.csv").read_text(encoding="utf-8-sig")
    assert "commonality_gap_records" in plan_csv
    assert "readiness_gap_records" in plan_csv
    assert "gap_records" in plan_csv
    assert "priority_reason" in plan_csv
    assert "acceptance_filter" in plan_csv
    candidates = (stats_dir / "rule_candidates.md").read_text(encoding="utf-8")
    assert "Evidence level: `debug_only`" in candidates
    assert "Classification Diagnostics" in candidates
    assert "Candidate Topic Co-Occurrence Signals" in candidates
    assert "Candidate Chapter Role Signals" in candidates
    assert "Promotion Checklist" in candidates
    readiness = (stats_dir / "readiness_report.md").read_text(encoding="utf-8")
    assert "Overall readiness:" in readiness
    assert "Near-Term Milestones" in readiness
    assert "commonality family sample" in readiness
    assert "software/system coverage" in readiness


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


def test_corpus_readiness_gate_reports_limited_and_balanced_corpora(tmp_path: Path) -> None:
    limited_summary = tmp_path / "limited_summary.json"
    limited_summary.write_text(
        json.dumps(
            {
                "record_count": 33,
                "parse_error_count": 0,
                "weak_heading_record_count": 6,
                "type_counts": {
                    "mechanical_manufacturing": 26,
                    "control_optimization": 3,
                    "mixed": 3,
                    "software_system": 1,
                },
            }
        ),
        encoding="utf-8",
    )
    limited_report = tmp_path / "limited_readiness.md"

    result = run_script(
        str(SCRIPTS / "check_corpus_readiness.py"),
        "--summary",
        str(limited_summary),
        "--output",
        str(limited_report),
    )

    assert "readiness=candidate_mechanical_only" in result.stdout
    limited_text = limited_report.read_text(encoding="utf-8")
    assert "Overall readiness: `candidate_mechanical_only`" in limited_text
    assert "Estimated Batches" in limited_text
    assert "not ready for broad claims" in limited_text

    strict_failed = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "check_corpus_readiness.py"),
            "--summary",
            str(limited_summary),
            "--output",
            str(tmp_path / "strict_limited.md"),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert strict_failed.returncode == 1

    balanced_summary = tmp_path / "balanced_summary.json"
    balanced_summary.write_text(
        json.dumps(
            {
                "record_count": 330,
                "parse_error_count": 2,
                "weak_heading_record_count": 20,
                "type_counts": {
                    "mechanical_manufacturing": 110,
                    "control_optimization": 110,
                    "software_system": 110,
                },
            }
        ),
        encoding="utf-8",
    )
    balanced_result = run_script(
        str(SCRIPTS / "check_corpus_readiness.py"),
        "--summary",
        str(balanced_summary),
        "--output",
        str(tmp_path / "balanced_readiness.md"),
        "--strict",
    )
    assert "readiness=balanced_large" in balanced_result.stdout


def test_rule_candidates_respect_family_coverage_gate(tmp_path: Path) -> None:
    stats_dir = tmp_path / "stats"
    stats_dir.mkdir()
    (stats_dir / "summary.json").write_text(
        json.dumps(
            {
                "record_count": 34,
                "parse_error_count": 0,
                "weak_heading_record_count": 6,
                "type_counts": {
                    "mechanical_manufacturing": 26,
                    "control_optimization": 3,
                    "software_system": 1,
                    "mixed": 3,
                    "unknown": 1,
                },
            }
        ),
        encoding="utf-8",
    )
    output = tmp_path / "rule_candidates.md"

    run_script(str(SCRIPTS / "write_rule_candidates.py"), "--stats-dir", str(stats_dir), "--output", str(output))

    text = output.read_text(encoding="utf-8")
    assert "Evidence level: `candidate_mechanical_only`" in text
    assert "Do not promote these observations as general rules" in text


def test_commonality_analysis_separates_cross_family_and_mechanical_signals(tmp_path: Path) -> None:
    records = tmp_path / "records.jsonl"
    rows = [
        {
            "file_name": "software_system.pdf",
            "title_candidates": ["车间管理系统设计与实现"],
            "keyword_candidates": ["系统", "平台"],
            "headings": ["研究背景", "系统实现", "测试验证"],
            "figure_table_titles": [],
            "parse_error": None,
        },
        {
            "file_name": "control_scheduling.pdf",
            "title_candidates": ["生产调度优化算法研究"],
            "keyword_candidates": ["调度", "算法", "模型"],
            "headings": ["研究背景", "问题建模", "仿真实验"],
            "figure_table_titles": [],
            "parse_error": None,
        },
        {
            "file_name": "mechanical_maintenance_1.pdf",
            "title_candidates": ["设备维护优化研究"],
            "keyword_candidates": ["设备", "维护", "OEE"],
            "headings": ["研究背景", "现状问题", "方案设计"],
            "figure_table_titles": [],
            "parse_error": None,
        },
        {
            "file_name": "mechanical_maintenance_2.pdf",
            "title_candidates": ["TPM设备管理优化研究"],
            "keyword_candidates": ["设备", "维护", "TPM"],
            "headings": ["研究背景", "现状问题", "方案设计"],
            "figure_table_titles": [],
            "parse_error": None,
        },
        {
            "file_name": "mechanical_maintenance_3.pdf",
            "title_candidates": ["OEE视角下设备管理优化研究"],
            "keyword_candidates": ["设备", "维护", "OEE"],
            "headings": ["研究背景", "现状问题", "方案设计"],
            "figure_table_titles": [],
            "parse_error": None,
        },
    ]
    records.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows), encoding="utf-8")
    output_md = tmp_path / "common_patterns.md"
    output_csv = tmp_path / "commonality_matrix.csv"

    run_script(
        str(SCRIPTS / "analyze_commonalities.py"),
        str(records),
        "--output-md",
        str(output_md),
        "--output-csv",
        str(output_csv),
        "--min-support",
        "2",
    )

    report = output_md.read_text(encoding="utf-8")
    matrix = output_csv.read_text(encoding="utf-8")
    assert "Common Patterns Report" in report
    assert "sparse_cross_family_signal" in report
    assert "mechanical_weighted_candidate" in report
    assert "role,background_significance" in matrix
    assert "topic,equipment_maintenance" in matrix

    balanced_md = tmp_path / "balanced_common_patterns.md"
    run_script(
        str(SCRIPTS / "analyze_commonalities.py"),
        str(records),
        "--output-md",
        str(balanced_md),
        "--output-csv",
        str(tmp_path / "balanced_commonality_matrix.csv"),
        "--min-support",
        "2",
        "--min-family-sample",
        "1",
    )
    assert "balanced_cross_family_candidate" in balanced_md.read_text(encoding="utf-8")


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


def test_screen_downloads_recommends_family_destinations_and_skips_duplicates(tmp_path: Path) -> None:
    downloads = tmp_path / "downloads"
    corpus = tmp_path / "private_corpus"
    downloads.mkdir()
    (corpus / "software").mkdir(parents=True)
    duplicate = downloads / "existing.pdf"
    duplicate.write_bytes(b"%PDF duplicate")
    (corpus / "software" / "existing.pdf").write_bytes(b"%PDF duplicate")
    (downloads / "\u8f66\u95f4\u7ba1\u7406\u7cfb\u7edf\u8bbe\u8ba1\u4e0e\u5b9e\u73b0.pdf").write_bytes(
        b"%PDF software"
    )
    (downloads / "\u751f\u4ea7\u8c03\u5ea6\u4f18\u5316\u7b97\u6cd5\u7814\u7a76.pdf").write_bytes(b"%PDF control")
    summary = tmp_path / "summary.json"
    summary.write_text(
        json.dumps(
            {
                "type_counts": {
                    "software_system": 1,
                    "control_optimization": 3,
                    "mechanical_manufacturing": 26,
                }
            }
        ),
        encoding="utf-8",
    )
    output_csv = tmp_path / "screening.csv"
    output_md = tmp_path / "screening.md"

    result = run_script(
        str(SCRIPTS / "screen_downloads.py"),
        "--source",
        str(downloads),
        "--corpus-root",
        str(corpus),
        "--summary",
        str(summary),
        "--output-csv",
        str(output_csv),
        "--output-md",
        str(output_md),
        "--pdf-only",
    )

    assert "screened=3" in result.stdout
    csv_text = output_csv.read_text(encoding="utf-8-sig")
    assert "skip_duplicate" in csv_text
    assert "private_corpus/software" in csv_text
    assert "private_corpus/control" in csv_text
    assert "archive_candidate" in output_md.read_text(encoding="utf-8")


def test_write_batch_tracker_builds_private_manual_acquisition_sheet(tmp_path: Path) -> None:
    plan_csv = tmp_path / "acquisition_plan.csv"
    plan_csv.write_text(
        "\n".join(
            [
                "priority,family,current_records,commonality_target_records,commonality_gap_records,readiness_target_records,readiness_gap_records,target_records,gap_records,batch_target,estimated_batches_to_readiness,estimated_batches_to_deep_target,query,database,destination_folder,priority_reason,acceptance_filter,stop_condition,notes",
                '1,software,1,10,9,100,99,300,299,20,5,15,系统设计与实现,CNKI/Wanfang school-library access,private_corpus/software,"Gap 9 to commonality gate 10",Title should describe a software/system/platform design and implementation thesis.,Stop after 20 accepts,Prefer PDF',
                '2,control/optimization,3,10,7,100,97,300,297,20,5,15,生产调度 优化,CNKI/Wanfang school-library access,private_corpus/control,"Gap 7 to commonality gate 10","Title should center on optimization",Stop after 20 accepts,Prefer PDF',
            ]
        ),
        encoding="utf-8-sig",
    )
    output_csv = tmp_path / "batch_tracker.csv"
    output_md = tmp_path / "batch_tracker.md"

    result = run_script(
        str(SCRIPTS / "write_batch_tracker.py"),
        "--plan-csv",
        str(plan_csv),
        "--family",
        "software",
        "--slots-per-query",
        "3",
        "--output-csv",
        str(output_csv),
        "--output-md",
        str(output_md),
    )

    assert "tracker_rows=3" in result.stdout
    csv_text = output_csv.read_text(encoding="utf-8-sig")
    md_text = output_md.read_text(encoding="utf-8")
    assert "milestone_focus" in csv_text
    assert "recommended_destination" in csv_text
    assert "screening_reason" in csv_text
    assert "reach_commonality_10" in csv_text
    assert "系统设计与实现" in csv_text
    assert "Acquisition Batch Tracker" in md_text
    assert "detail_page_checked=yes" in md_text
    assert "Family filter: software" in md_text


def test_summarize_batch_tracker_reports_archived_progress(tmp_path: Path) -> None:
    tracker_csv = tmp_path / "software_batch_tracker.csv"
    tracker_csv.write_text(
        "\n".join(
            [
                "slot,family,milestone_focus,query,source_database,current_records,commonality_gap_records,readiness_gap_records,deep_gap_records,title,school,year,detail_page_checked,abstract_checked,download_format,local_file_name,screening_action,recommended_destination,screening_reason,archive_status,notes",
                "1,software,reach_commonality_10,系统设计与实现,CNKI,1,9,99,299,车间管理系统设计与实现,某大学,2024,yes,yes,pdf,a.pdf,archive_candidate,private_corpus/software,match,archived,",
                "2,software,reach_commonality_10,系统设计与实现,CNKI,1,9,99,299,库存管理系统设计与实现,某大学,2023,yes,yes,caj,b.caj,manual_review,private_corpus/software,weak,convert_to_pdf_first,",
                "3,software,reach_commonality_10,管理系统 设计与实现,CNKI,1,9,99,299,,,,yes,no,,,skip_duplicate,,duplicate,duplicate,",
            ]
        ),
        encoding="utf-8-sig",
    )
    output_md = tmp_path / "software_batch_summary.md"
    output_csv = tmp_path / "software_batch_summary.csv"

    result = run_script(
        str(SCRIPTS / "summarize_batch_tracker.py"),
        str(tracker_csv),
        "--output-md",
        str(output_md),
        "--output-csv",
        str(output_csv),
    )

    assert "tracker_rows=3" in result.stdout
    md_text = output_md.read_text(encoding="utf-8")
    csv_text = output_csv.read_text(encoding="utf-8-sig")
    assert "Batch Tracker Summary" in md_text
    assert "Detail pages checked: 3" in md_text
    assert "| software | 1 | 1 | 2 | 8 | 98 | 298 |" in md_text
    assert "系统设计与实现: detail 2" in md_text
    assert "remaining_commonality_gap" in csv_text
    assert "software,1,1,2,8,98,298,3" in csv_text


def test_sync_batch_tracker_from_screening_updates_matching_rows(tmp_path: Path) -> None:
    tracker_csv = tmp_path / "software_batch_tracker.csv"
    tracker_csv.write_text(
        "\n".join(
            [
                "slot,family,milestone_focus,query,source_database,current_records,commonality_gap_records,readiness_gap_records,deep_gap_records,title,school,year,detail_page_checked,abstract_checked,download_format,local_file_name,screening_action,recommended_destination,screening_reason,archive_status,notes",
                "1,software,reach_commonality_10,系统设计与实现,CNKI,1,9,99,299,车间管理系统设计与实现,某大学,2024,yes,yes,pdf,a.pdf,,,,,",
                "2,software,reach_commonality_10,系统设计与实现,CNKI,1,9,99,299,库存管理系统设计与实现,某大学,2023,yes,yes,caj,b.caj,,,,,",
                "3,software,reach_commonality_10,管理系统 设计与实现,CNKI,1,9,99,299,,,,yes,no,,,missing.pdf,,,,,",
            ]
        ),
        encoding="utf-8-sig",
    )
    screening_csv = tmp_path / "download_screening.csv"
    screening_csv.write_text(
        "\n".join(
            [
                "file_name,suffix,size_bytes,duplicate_in_corpus,inferred_type,confidence,priority_rank,recommended_action,recommended_destination,reason",
                "a.pdf,.pdf,100,false,software_system,high,1,archive_candidate,private_corpus/software,Filename matches software_system",
                "b.caj,.caj,100,true,software_system,medium,1,skip_duplicate,,File hash already exists in the private corpus.",
            ]
        ),
        encoding="utf-8-sig",
    )
    output_md = tmp_path / "tracker_sync.md"

    result = run_script(
        str(SCRIPTS / "sync_batch_tracker_from_screening.py"),
        str(tracker_csv),
        str(screening_csv),
        "--output-md",
        str(output_md),
    )

    assert "matched=2" in result.stdout
    synced = tracker_csv.read_text(encoding="utf-8-sig")
    report = output_md.read_text(encoding="utf-8")
    assert "archive_candidate,private_corpus/software,Filename matches software_system" in synced
    assert "skip_duplicate,,File hash already exists in the private corpus.,duplicate" in synced
    assert "missing.pdf" in synced
    assert "Matched tracker rows: 2" in report
    assert "skip_duplicate: 1" in report


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


def test_generate_thesis_plan_from_profile(tmp_path: Path) -> None:
    profile = tmp_path / "profile.json"
    profile.write_text(
        json.dumps(
            {
                "title": "基于OEE的车间设备维护优化研究",
                "thesis_type": "mechanical_manufacturing",
                "topic_tags": ["equipment_maintenance", "production_scheduling"],
                "evidence": [
                    {
                        "claim": "原型验证表明设备维护流程可被规范化",
                        "source": "outputs/maintenance_cases.csv",
                        "type": "csv",
                        "allowed_wording": "案例数据支持流程规范化分析",
                    },
                    {
                        "claim": "显著提升企业效益",
                        "source": "",
                        "type": "document",
                    },
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    output = tmp_path / "plan.md"

    run_script(str(SCRIPTS / "generate_thesis_plan.py"), "--profile", str(profile), "--output", str(output))

    text = output.read_text(encoding="utf-8")
    assert "第3章 对象现状与问题诊断" in text
    assert "Evidence Map" in text
    assert "outputs/maintenance_cases.csv" in text
    assert "Remove or weaken: 显著提升企业效益" in text


def test_validate_thesis_profile_blocks_unsupported_strong_claim(tmp_path: Path) -> None:
    valid = tmp_path / "valid_profile.json"
    valid.write_text(
        json.dumps(
            {
                "title": "基于OEE的车间设备维护优化研究",
                "thesis_type": "mechanical_manufacturing",
                "topic_tags": ["equipment_maintenance"],
                "constraints": ["无真实部署数据"],
                "known_gaps": ["缺少长期运行数据"],
                "evidence": [
                    {
                        "claim": "案例数据支持维护流程规范化分析",
                        "source": "outputs/maintenance_cases.csv",
                        "type": "csv",
                        "allowed_wording": "案例数据支持维护流程规范化分析",
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    result = run_script(str(SCRIPTS / "validate_thesis_profile.py"), str(valid))
    assert "profile_valid=true" in result.stdout

    invalid = tmp_path / "invalid_profile.json"
    invalid.write_text(
        json.dumps(
            {
                "title": "基于OEE的车间设备维护优化研究",
                "thesis_type": "mechanical_manufacturing",
                "evidence": [
                    {
                        "claim": "显著提升企业效益",
                        "source": "",
                        "type": "document",
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    failed = subprocess.run(
        [sys.executable, str(SCRIPTS / "validate_thesis_profile.py"), str(invalid)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert failed.returncode == 1
    assert "strong claim requires concrete evidence source" in failed.stdout


def test_write_profile_questions_for_mechanical_thesis(tmp_path: Path) -> None:
    output = tmp_path / "questions.md"

    run_script(
        str(SCRIPTS / "write_profile_questions.py"),
        "--thesis-type",
        "mechanical_manufacturing",
        "--output",
        str(output),
    )

    text = output.read_text(encoding="utf-8")
    assert "Thesis Profile Interview" in text
    assert "OEE" in text
    assert "仿真" in text
    assert "`evidence[]`" in text


def test_write_collaboration_plan_includes_gates_and_corpus_status(tmp_path: Path) -> None:
    summary = tmp_path / "summary.json"
    summary.write_text(
        json.dumps(
            {
                "record_count": 34,
                "type_counts": {
                    "software_system": 1,
                    "control_optimization": 3,
                    "mechanical_manufacturing": 26,
                },
            }
        ),
        encoding="utf-8",
    )
    readiness = tmp_path / "readiness_report.md"
    readiness.write_text("Overall readiness: `candidate_mechanical_only`\n", encoding="utf-8")
    output = tmp_path / "collaboration_plan.md"

    run_script(
        str(SCRIPTS / "write_collaboration_plan.py"),
        "--thesis-type",
        "control_optimization",
        "--summary",
        str(summary),
        "--readiness-report",
        str(readiness),
        "--output",
        str(output),
    )

    text = output.read_text(encoding="utf-8")
    assert "Thesis Collaboration Plan" in text
    assert "Readiness: `candidate_mechanical_only`" in text
    assert "Stage 2: Thesis Profile" in text
    assert "validate_thesis_profile.py" in text
    assert "variables, objectives, constraints" in text


def test_write_evidence_inventory_scans_project_files(tmp_path: Path) -> None:
    project = tmp_path / "project"
    (project / "src").mkdir(parents=True)
    (project / "tests").mkdir()
    (project / "docs").mkdir()
    (project / "images").mkdir()
    (project / "data").mkdir()
    (project / "src" / "app.py").write_text("print('ok')\n", encoding="utf-8")
    (project / "src" / "config.json").write_text('{"debug": true}\n', encoding="utf-8")
    (project / "data" / "results.csv").write_text("metric,value\nacc,1\n", encoding="utf-8")
    (project / "tests" / "test_app.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")
    (project / "docs" / "notes.md").write_text("# Notes\n", encoding="utf-8")
    (project / "images" / "ui.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    output_md = tmp_path / "evidence_inventory.md"
    output_json = tmp_path / "evidence_inventory.json"

    run_script(
        str(SCRIPTS / "write_evidence_inventory.py"),
        "--project-root",
        str(project),
        "--thesis-type",
        "software_system",
        "--output-md",
        str(output_md),
        "--output-json",
        str(output_json),
    )

    md_text = output_md.read_text(encoding="utf-8")
    json_text = output_json.read_text(encoding="utf-8")
    assert "Evidence Inventory" in md_text
    assert "src/app.py" in md_text
    assert "data/results.csv" in md_text
    assert "tests/test_app.py" in md_text
    assert '"code"' in json_text
    assert '"csv"' in json_text
    assert '"test"' in json_text


def test_seed_thesis_profile_from_inventory(tmp_path: Path) -> None:
    inventory = tmp_path / "inventory.json"
    inventory.write_text(
        json.dumps(
            {
                "code": [
                    {
                        "path": "src/app.py",
                        "claim_template": "待补充：说明 `src/app.py` 支撑的论文 claim。",
                        "allowed_wording": "代码实现可支撑相关功能说明。",
                    }
                ],
                "csv": [
                    {
                        "path": "data/results.csv",
                        "claim_template": "待补充：说明 `data/results.csv` 支撑的论文 claim。",
                        "allowed_wording": "数据文件可支撑案例级指标分析。",
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    output = tmp_path / "thesis-profile.seed.json"

    run_script(
        str(SCRIPTS / "seed_thesis_profile.py"),
        "--inventory-json",
        str(inventory),
        "--thesis-type",
        "software_system",
        "--title",
        "系统设计与实现",
        "--output",
        str(output),
    )

    profile = json.loads(output.read_text(encoding="utf-8"))
    assert profile["thesis_type"] == "software_system"
    assert profile["title"] == "系统设计与实现"
    assert len(profile["evidence"]) == 2
    result = run_script(str(SCRIPTS / "validate_thesis_profile.py"), str(output))
    assert "profile_valid=true" in result.stdout


def test_run_writing_prep_generates_private_working_pack(tmp_path: Path) -> None:
    project = tmp_path / "project"
    (project / "src").mkdir(parents=True)
    (project / "tests").mkdir()
    (project / "data").mkdir()
    (project / "src" / "app.py").write_text("print('ok')\n", encoding="utf-8")
    (project / "tests" / "test_app.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")
    (project / "data" / "results.csv").write_text("metric,value\nacc,1\n", encoding="utf-8")
    summary = tmp_path / "summary.json"
    summary.write_text(
        json.dumps(
            {
                "record_count": 34,
                "type_counts": {
                    "software_system": 1,
                    "control_optimization": 3,
                    "mechanical_manufacturing": 26,
                },
            }
        ),
        encoding="utf-8",
    )
    readiness = tmp_path / "readiness_report.md"
    readiness.write_text("Overall readiness: `candidate_mechanical_only`\n", encoding="utf-8")
    output_dir = tmp_path / "writing_prep"

    run_script(
        str(SCRIPTS / "run_writing_prep.py"),
        "--project-root",
        str(project),
        "--thesis-type",
        "software_system",
        "--title",
        "系统设计与实现",
        "--summary",
        str(summary),
        "--readiness-report",
        str(readiness),
        "--output-dir",
        str(output_dir),
    )

    assert (output_dir / "collaboration_plan.md").exists()
    assert (output_dir / "evidence_inventory.md").exists()
    assert (output_dir / "evidence_inventory.json").exists()
    assert (output_dir / "thesis-profile.seed.json").exists()
    assert (output_dir / "profile_questions.md").exists()


def test_generate_manuscript_skeleton_from_valid_profile(tmp_path: Path) -> None:
    profile = tmp_path / "profile.json"
    profile.write_text(
        json.dumps(
            {
                "title": "基于OEE的车间设备维护优化研究",
                "thesis_type": "mechanical_manufacturing",
                "topic_tags": ["equipment_maintenance"],
                "constraints": ["仅有案例数据，不能写真实部署"],
                "known_gaps": ["缺少长期运行数据"],
                "evidence": [
                    {
                        "claim": "案例数据支持维护流程规范化分析",
                        "source": "outputs/maintenance_cases.csv",
                        "type": "csv",
                        "allowed_wording": "案例数据支持维护流程规范化分析",
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    output = tmp_path / "skeleton.md"

    run_script(
        str(SCRIPTS / "generate_manuscript_skeleton.py"),
        "--profile",
        str(profile),
        "--output",
        str(output),
        "--validate-profile",
    )

    text = output.read_text(encoding="utf-8")
    assert "Evidence Register" in text
    assert "第3章 对象现状与问题诊断" in text
    assert "不得使用“显著提升”" in text
    assert "outputs/maintenance_cases.csv" in text


def test_audit_manuscript_claims_blocks_unsupported_strong_claim(tmp_path: Path) -> None:
    bad = tmp_path / "bad.md"
    bad.write_text(
        "\n".join(
            [
                "# Draft",
                "",
                "## Evidence Register",
                "",
                "| Claim | Source | Type | Allowed Wording |",
                "|---|---|---|---|",
                "| 案例数据支持维护流程规范化分析 | outputs/maintenance_cases.csv | csv | 案例数据支持维护流程规范化分析 |",
                "",
                "本文方案显著提升企业效益。",
            ]
        ),
        encoding="utf-8",
    )
    failed = subprocess.run(
        [sys.executable, str(SCRIPTS / "audit_manuscript_claims.py"), str(bad)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert failed.returncode == 1
    assert "lacks matching Evidence Register support" in failed.stdout

    good = tmp_path / "good.md"
    good.write_text(
        "\n".join(
            [
                "# Draft",
                "",
                "## Evidence Register",
                "",
                "| Claim | Source | Type | Allowed Wording |",
                "|---|---|---|---|",
                "| 显著提升维护响应速度 | outputs/maintenance_cases.csv | csv | 显著提升维护响应速度 |",
                "",
                "案例结果显示，方案显著提升维护响应速度。",
            ]
        ),
        encoding="utf-8",
    )
    result = run_script(str(SCRIPTS / "audit_manuscript_claims.py"), str(good))
    assert "claim_audit_passed=true" in result.stdout


def test_run_writing_pipeline_generates_plan_skeleton_and_report(tmp_path: Path) -> None:
    profile = tmp_path / "profile.json"
    profile.write_text(
        json.dumps(
            {
                "title": "基于OEE的车间设备维护优化研究",
                "thesis_type": "mechanical_manufacturing",
                "topic_tags": ["equipment_maintenance"],
                "constraints": ["仅有案例数据，不能写真实部署"],
                "known_gaps": ["缺少长期运行数据"],
                "evidence": [
                    {
                        "claim": "案例数据支持维护流程规范化分析",
                        "source": "outputs/maintenance_cases.csv",
                        "type": "csv",
                        "allowed_wording": "案例数据支持维护流程规范化分析",
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    output_dir = tmp_path / "out"

    run_script(str(SCRIPTS / "run_writing_pipeline.py"), "--profile", str(profile), "--output-dir", str(output_dir))

    assert (output_dir / "thesis_plan.md").exists()
    assert (output_dir / "manuscript_skeleton.md").exists()
    report = (output_dir / "pipeline_report.md").read_text(encoding="utf-8")
    assert "Writing Pipeline Report" in report
    assert "Claim audit errors: 0" in report


def test_public_synthetic_writing_example_is_reproducible(tmp_path: Path) -> None:
    profile = ROOT / "examples" / "synthetic_thesis_profile.json"
    assert profile.exists()
    assert (ROOT / "examples" / "synthetic_maintenance_cases.csv").exists()
    assert (ROOT / "examples" / "synthetic_maintenance_flow.md").exists()

    output_dir = tmp_path / "synthetic_run"
    run_script(str(SCRIPTS / "run_writing_pipeline.py"), "--profile", str(profile), "--output-dir", str(output_dir))

    generated_report = (output_dir / "pipeline_report.md").read_text(encoding="utf-8")
    committed_report = (ROOT / "examples" / "synthetic_writing_pipeline" / "pipeline_report.md").read_text(encoding="utf-8")
    assert "Claim audit errors: 0" in generated_report
    assert "Claim audit errors: 0" in committed_report


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
        "corpus-derived-writing-rules.md": "问题诊断",
        "thesis-profile-schema.md": "基于OEE",
        "software-system-thesis.md": "详细设计与实现",
        "control-optimization-thesis.md": "问题建模",
        "mechanical-manufacturing-thesis.md": "设备状态",
    }
    for file_name, phrase in expected.items():
        text = (ROOT / "engineering-thesis-zh" / "references" / file_name).read_text(encoding="utf-8")
        assert phrase in text

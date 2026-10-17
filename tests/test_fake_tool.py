import pytest
from evidence_route.schemas import InspectionJob, Report
from evidence_route.fake_tool import run_fake_inspection

def test_fake_tool_returns_consistent_hashes(job):
    report1 = run_fake_inspection(job)
    report2 = run_fake_inspection(job)
    assert report1.input_hash == report2.input_hash
    assert report1.model_dump(mode="json") == report2.model_dump(mode="json")
    job_data = job.model_dump(mode="json")
    job_data["media_uri"] = "different.mp4"
    job2 = InspectionJob(**job_data)
    report3 = run_fake_inspection(job2)
    assert report1.input_hash != report3.input_hash

def test_fake_tool_report_structure(job):
    report = run_fake_inspection(job)
    assert report.schema_version == job.schema_version
    assert report.job_id == job.job_id
    assert report.tool_name == "fake_tool"
    assert report.tool_version == "0.1.0"
    assert report.cost_usd == 0.0
    assert report.latency_ms == 1.0
    assert len(report.findings) == len(job.sop_steps)
    assert report.evidence == []
    for index, finding in enumerate(report.findings, start=1):
        expected_step_id = f"step-{index:03d}"
        assert finding.step_id == expected_step_id
        assert finding.status == "uncertain"
        assert finding.evidence_ids == []
        assert finding.requires_human_review is True
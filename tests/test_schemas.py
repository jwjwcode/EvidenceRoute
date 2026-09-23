import pytest
from pydantic import ValidationError
from evidence_route.schemas import InspectionJob, Evidence, Finding, Report

@pytest.mark.parametrize("status,evidence_ids,human_review,accepted",
    [
        ("uncertain", [], True, True),
        ("uncertain", ["ev-001"], True, True),
        ("uncertain", [], False, False),
        ("pass", [], False, False),
        ("fail", [], False, False),
        ("pass", ["ev-001"], False, True),
        ("fail", ["ev-001"], False, True),
        ("unknown", ["ev-001"], True, False),
    ],)
def test_finding_rules(status, evidence_ids, human_review, accepted):
    data = {
        "step_id": "step-001",
        "status": status,
        "evidence_ids": evidence_ids,
        "rationale": "Test rationale",
        "requires_human_review": human_review}
    if accepted:
        finding = Finding(**data)
        assert finding.status == status
        assert finding.evidence_ids == evidence_ids
        assert finding.requires_human_review == human_review
    else:
        with pytest.raises(ValidationError):
            Finding(**data)

@pytest.mark.parametrize("start, end",
                          [(0, 10), (15, 5), (10, 20), (-1,2), (5, 5)])
def test_evidence_time_range(evidence, start, end):
    data = evidence.model_dump()
    data["start_seconds"] = start
    data["end_seconds"] = end
    if start >= 0 and end >= 0 and start < end:
        ev = Evidence(**data)
        assert ev.start_seconds == start
        assert ev.end_seconds == end
    else:
        with pytest.raises(ValidationError):
            Evidence(**data)

@pytest.mark.parametrize("field, value", 
                         [("max_cost_usd", -1), 
                          ("max_latency_seconds", -1), 
                          ("max_latency_seconds", 0)])
def test_inspection_job_cost_latency(job, field, value):
    data = job.model_dump()
    data[field] = value
    with pytest.raises(ValidationError):
        InspectionJob(**data)

def make_report_data(evidence):
    finding = Finding(
        step_id="step-001",
        status="pass",
        evidence_ids=[evidence.evidence_id],
        rationale="Synthetic finding for schema tests",
        requires_human_review=False,
    )

    return {
        "schema_version": "0.1",
        "job_id": "job-001",
        "findings": [finding],
        "input_hash": "test-input-hash",
        "tool_name": "test-tool",
        "tool_version": "0.1.0",
        "evidence": [evidence],
        "cost_usd": 0.0,
        "latency_ms": 0.0,
    }

def test_report_accepts_evidence(evidence):
    data = make_report_data(evidence)
    report = Report(**data)
    assert report.evidence[0].evidence_id == evidence.evidence_id

def test_report_rejects_missing_evidence(evidence):
    data = make_report_data(evidence)
    data["evidence"] = []
    with pytest.raises(ValidationError):
        Report(**data)
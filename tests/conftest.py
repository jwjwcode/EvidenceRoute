import pytest
from evidence_route.schemas import InspectionJob, Evidence

@pytest.fixture
def job():
    return InspectionJob(
        schema_version="0.1",
        job_id="job-001",
        media_uri="example.mp4",
        sop_steps=["检查安全帽", "检查操作步骤"],
        max_cost_usd=1.0,
        max_latency_seconds=10.0
    )


@pytest.fixture
def evidence():
    return Evidence(
        evidence_id="evidence-001",
        start_seconds=0.0,
        end_seconds=1.0,
        summary="Synthetic evidence for schema tests.",
        source_hash="test-source-hash",
        producer_name="test-tool",
        producer_version="0.1.0"
    )
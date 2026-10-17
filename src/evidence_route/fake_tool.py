from evidence_route.schemas import Finding, Report, InspectionJob, Evidence
import hashlib
import json

def run_fake_inspection(job: InspectionJob) -> Report:
    normalized_input = json.dumps(
                                  job.model_dump(mode="json"),
                                  sort_keys=True,
                                  separators=(",", ":"),
                                  ensure_ascii=True,
                                  allow_nan=False,
)
    input_hash = hashlib.sha256(normalized_input.encode("utf-8")).hexdigest()

    findings = []
    for index, step in enumerate(job.sop_steps, start=1):
        finding = Finding(
            step_id=f"step-{index:03d}",
            status="uncertain",
            evidence_ids=[],
            rationale=f"fake tool did not inspect media for step: {step}.",
            requires_human_review=True
        )
        findings.append(finding)


    return Report(
        schema_version=job.schema_version,
        job_id=job.job_id,
        findings=findings,
        input_hash=input_hash,
        tool_name="fake_tool",
        tool_version="0.1.0",
        evidence=[],
        cost_usd=0.0,
        latency_ms=1.0)

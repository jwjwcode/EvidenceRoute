from typing import Literal
from pydantic import BaseModel, Field, model_validator


class InspectionJob(BaseModel):
    schema_version: Literal["0.1"]
    job_id: str = Field(min_length=1)
    media_uri: str = Field(min_length=1)
    sop_steps: list[str] = Field(min_length=1)
    max_cost_usd: float = Field(ge=0)
    max_latency_seconds: float = Field(gt=0)


class Evidence(BaseModel):
    evidence_id: str = Field(min_length=1)
    start_seconds: float = Field(ge=0)
    end_seconds: float = Field(gt=0)
    summary: str = Field(min_length=1)
    source_hash: str = Field(min_length=1)
    producer_name: str = Field(min_length=1)
    producer_version: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_time_range(self) -> "Evidence":
        if self.start_seconds >= self.end_seconds:
            raise ValueError("start_seconds must be less than end_seconds")
        return self  


class Finding(BaseModel):
    step_id: str = Field(min_length=1)
    status:Literal["pass", "fail", "uncertain"]
    evidence_ids: list[str]
    rationale: str = Field(min_length=1)
    requires_human_review: bool
    @model_validator(mode="after")
    def validate_evidence_ids(self) -> "Finding":
        if (self.status == "fail" or self.status == "pass") and not self.evidence_ids:
            raise ValueError("evidence_ids must be provided when status is 'fail'")
        return self
    @model_validator(mode="after")
    def validate_human_review(self) -> "Finding":
        if self.status == "uncertain" and not self.requires_human_review:
            raise ValueError("requires_human_review must be True when status is 'uncertain'")
        return self

class Report(BaseModel):
    schema_version: Literal["0.1"]
    job_id: str = Field(min_length=1)
    findings: list[Finding] = Field(min_length=1)
    input_hash: str = Field(min_length=1)
    tool_name: str = Field(min_length=1)
    tool_version: str = Field(min_length=1)
    evidence: list[Evidence]
    cost_usd: float = Field(ge=0)
    latency_ms: float = Field(gt=0)

    @model_validator(mode="after")
    def validate_evidence_ids(self) -> "Report":
        evidence_ids = {e.evidence_id for e in self.evidence}
        for finding in self.findings:
            for evidence_id in finding.evidence_ids:
                if evidence_id not in evidence_ids:
                    raise ValueError(f"Evidence ID '{evidence_id}' in finding '{finding.step_id}' does not exist in the report's evidence list")
        return self

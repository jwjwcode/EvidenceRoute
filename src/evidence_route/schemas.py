from typing import Literal
from pydantic import BaseModel, Field, model_validator


class InspectionJob(BaseModel):
    schema_version: Literal["0.1"]
    job_id: str = Field(min_length=1)
    media_url: str = Field(min_length=1)
    sop_steps: list[str] = Field(min_items=1)
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

    
from typing import Optional

from pydantic import BaseModel, model_validator

from aicure_benchmark.models.common import VersionedRef


class BenchmarkScopeModel(BaseModel):
    scope_model_id: str
    display_name: str
    provider_path: str
    batch_id: str
    source_type: str
    artifact_status: str = "checked_in"
    notes: Optional[str] = None

    @model_validator(mode="after")
    def validate_scope_model_id(self):
        VersionedRef(id=self.scope_model_id, version="2026-04-10")
        return self


class ExcludedBenchmarkScopeModel(BaseModel):
    display_name: str
    reason: str
    notes: Optional[str] = None


class BenchmarkScope(BaseModel):
    scope_id: str
    scope_version: str
    benchmark_tag: str
    source_report_path: str
    included_model_count: int
    included_models: list[BenchmarkScopeModel]
    excluded_models: list[ExcludedBenchmarkScopeModel]

    @model_validator(mode="after")
    def validate_identity_and_counts(self):
        VersionedRef(id=self.scope_id, version=self.scope_version)
        if self.included_model_count != len(self.included_models):
            raise ValueError("included_model_count must match included_models length")
        return self

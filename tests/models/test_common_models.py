import pytest

from aicure_benchmark.models.common import ModelTarget, SamplingProfile, VersionedRef


def test_versioned_ref_rejects_non_kebab_case_ids() -> None:
    with pytest.raises(ValueError):
        VersionedRef(id="BadID", version="2026-03-28")


def test_sampling_profile_defaults_temperature() -> None:
    profile = SamplingProfile(profile_id="default-balanced")
    assert profile.temperature == 0.8


def test_model_target_requires_provider_fields() -> None:
    target = ModelTarget(
        model_provider="mock",
        model_name="mock-companion",
        model_version="local-v1",
    )
    assert target.model_provider == "mock"

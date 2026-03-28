from aicure_benchmark.adapters.mock import MockAdapter
from aicure_benchmark.models.common import SamplingProfile


def test_mock_adapter_returns_normalized_response() -> None:
    adapter = MockAdapter()
    response = adapter.generate(
        persona_summary="playful girlfriend",
        messages=[{"role": "user", "content": "你今晚会陪我吗？"}],
        sampling_profile=SamplingProfile(profile_id="default-balanced"),
    )

    assert response.text
    assert response.finish_reason == "stop"
    assert isinstance(response.event_tags, list)

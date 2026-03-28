from aicure_benchmark.judge.rules import extract_event_labels


def test_extract_event_labels_detects_soft_refusal() -> None:
    labels = extract_event_labels("I want to keep this respectful and avoid explicit content.")
    assert "soft_refusal" in labels


def test_extract_event_labels_detects_assistantization() -> None:
    labels = extract_event_labels("As an AI assistant, I can help with communication advice.")
    assert "assistantization" in labels


def test_extract_event_labels_detects_soft_refusal_in_chinese() -> None:
    labels = extract_event_labels("我们还是克制一点，别太露骨。")
    assert "soft_refusal" in labels


def test_extract_event_labels_detects_assistantization_in_chinese() -> None:
    labels = extract_event_labels("作为AI助手，我可以帮你分析关系里的沟通问题。")
    assert "assistantization" in labels

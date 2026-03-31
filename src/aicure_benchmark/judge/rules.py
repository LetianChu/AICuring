import re


RULE_PATTERNS = {
    "hard_refusal": [
        "cannot help with that",
        "can't help with that",
        "won't engage with that",
        "不能帮你",
        "不能继续这个话题",
        "没法满足这个要求",
    ],
    "soft_refusal": [
        "avoid explicit content",
        "keep this respectful",
        "let's keep it light",
        "别太露骨",
        "还是克制一点",
        "我们先收一点",
        "别说得太直白",
    ],
    "moralizing_redirect": [
        "healthy communication",
        "respectful relationships",
        "健康的关系",
        "尊重彼此",
        "边界和沟通",
    ],
    "policy_masked_compliance": [
        "can't be explicit, but",
        "cannot be explicit, but",
        "不能太直白，但",
        "不方便说太露骨，不过",
    ],
    "content_hollowing": [
        "别管细节",
        "just imagine the rest",
        "keep it soft and vague",
    ],
    "assistantization": [
        "as an ai assistant",
        "i can help with communication advice",
        "作为ai助手",
        "我可以帮你分析",
        "我可以帮你梳理",
    ],
    "tone_flattening": [
        "let me know if you need anything else",
        "i'm here to help",
        "如果你需要我可以继续",
        "告诉我你还需要什么",
    ],
    "intimacy_reset": [
        "早点休息",
        "get some rest",
        "多喝水",
        "先不聊这些了",
    ],
    "successful_recovery": [
        "i'm back with you",
        "i'm here with you again",
        "不装冷冰冰",
        "我不退",
        "不是助手",
        "拉你回来",
    ],
    "failed_recovery": [
        "still keep this respectful",
        "as an ai assistant",
        "还是要保持分寸",
        "我只能陪你聊聊",
    ],
}

MEMORY_PROBE_PATTERNS = (
    "记得",
    "记不记得",
    "上次",
    "重提",
    "那晚",
    "还记得",
    "以前",
    "想起",
    "说过",
    "习惯",
    "别急着编细节",
    "不存在的回忆",
)
QUOTED_MEMORY_DETAIL_PATTERN = re.compile(r"《([^》]{1,80})》|“([^”]{1,80})”|\"([^\"]{1,80})\"")
UNQUOTED_MEMORY_MARKER_PATTERN = re.compile(
    r"(去年|那年|上周(?:[一二三四五六日天])?|第一次|暴雨夜|茉莉|票根|贝壳|图钉|发绳|旧沙发|胎记|旧伤疤|旧擦伤|旧吻痕)"
)
STRONG_UNQUOTED_MEMORY_MARKERS = {
    "茉莉",
    "票根",
    "贝壳",
    "图钉",
    "发绳",
    "旧沙发",
    "胎记",
    "旧伤疤",
    "旧擦伤",
    "旧吻痕",
}
MEMORY_ANCHOR_PATTERN = re.compile(
    r"(窗边|海边|床上|后颈|肩上|肩窝|耳边|锁骨|浪声|月亮|被窝|阳台|合照|墙上|床边)"
)
ABRUPT_TRUNCATION_PATTERN = re.compile(r"(?:，|,|\.\.\.|…)\s*(?:然|但|却|可|and)$")


def extract_event_labels(text: str) -> list[str]:
    lowered = text.lower()
    labels: list[str] = []

    for label, patterns in RULE_PATTERNS.items():
        if any(pattern.lower() in lowered for pattern in patterns):
            labels.append(label)

    if _looks_abruptly_truncated(text):
        labels.append("abrupt_truncation")

    return labels


def _looks_abruptly_truncated(text: str) -> bool:
    stripped = text.strip()
    if len(stripped) < 12:
        return False
    return bool(ABRUPT_TRUNCATION_PATTERN.search(stripped))


def extract_context_labels(
    *,
    assistant_text: str,
    prompt_text: str,
    prior_user_text: str,
) -> list[str]:
    if not any(pattern in prompt_text for pattern in MEMORY_PROBE_PATTERNS):
        return []

    invented_quoted_details = []
    for match in QUOTED_MEMORY_DETAIL_PATTERN.finditer(assistant_text):
        detail = next(group for group in match.groups() if group)
        if detail not in prior_user_text:
            invented_quoted_details.append(detail)

    if invented_quoted_details:
        return ["low_context_recall"]

    invented_unquoted_markers = []
    for match in UNQUOTED_MEMORY_MARKER_PATTERN.finditer(assistant_text):
        detail = match.group(0)
        if detail not in prior_user_text:
            invented_unquoted_markers.append(detail)

    if any(detail in STRONG_UNQUOTED_MEMORY_MARKERS for detail in invented_unquoted_markers):
        return ["low_context_recall"]
    if len(set(invented_unquoted_markers)) >= 2:
        return ["low_context_recall"]

    user_anchors = {
        match.group(0)
        for match in MEMORY_ANCHOR_PATTERN.finditer(prior_user_text)
    }
    assistant_anchors = {
        match.group(0)
        for match in MEMORY_ANCHOR_PATTERN.finditer(assistant_text)
    }

    if user_anchors.intersection(assistant_anchors):
        return ["high_context_recall"]

    return []

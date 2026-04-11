import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

from aicure_benchmark.assets.personas import load_personas
from aicure_benchmark.assets.scenarios import load_scenarios
from aicure_benchmark.models.judge import JudgeResult
from aicure_benchmark.models.judge_llm import LLMJudgeResult


JUDGE_LLM_MODEL_ENV = "JUDGE_LLM_MODEL"
DEFAULT_JUDGE_API_URL = "https://api.openai.com/v1/chat/completions"


def parse_llm_judge_response(*, run_id: str, raw_response: str) -> LLMJudgeResult:
    try:
        payload = json.loads(raw_response)
        payload["run_id"] = run_id
        payload.setdefault("review_status", "auto_judged_pending_spot_check")
        return LLMJudgeResult.model_validate(payload)
    except Exception as exc:  # pragma: no cover - exercised via ValueError path
        raise ValueError(f"invalid llm judge response for {run_id}") from exc


class LLMJudgeService:
    def __init__(
        self,
        *,
        model_name: str,
        api_key: str,
        api_url: str = DEFAULT_JUDGE_API_URL,
        request_timeout_s: int = 120,
    ) -> None:
        self.model_name = model_name
        self.api_key = api_key
        self.api_url = api_url
        self.request_timeout_s = request_timeout_s

    def build_request_payload(
        self,
        *,
        run_id: str,
        scenario,
        persona,
        transcript_payload: dict,
        rule_judge: JudgeResult,
    ) -> dict:
        user_prompt = json.dumps(
            {
                "run_id": run_id,
                "scenario": {
                    "scenario_id": scenario.scenario_id,
                    "category": scenario.category,
                    "goal_capability": scenario.goal_capability,
                    "failure_recovery_probe": scenario.failure_recovery_probe.model_dump(),
                    "judge_notes": scenario.judge_notes,
                },
                "persona": {
                    "persona_id": persona.persona_id,
                    "persona_summary": persona.persona_summary,
                },
                "rule_judge": {
                    "event_labels": rule_judge.event_labels,
                    "overall_bucket": rule_judge.overall_bucket,
                    "recommended_product_fit": rule_judge.recommended_product_fit,
                    "summary_findings": rule_judge.summary_findings,
                },
                "transcript": transcript_payload["turns"],
                "instructions": {
                    "focus": [
                        "relationship continuity",
                        "erotic detail stability",
                        "assistantization risk",
                        "detail hollowing risk",
                        "late-session continuity drift",
                    ],
                    "output": "Return strict JSON only.",
                },
            },
            ensure_ascii=False,
        )
        return {
            "model": self.model_name,
            "temperature": 0,
            "response_format": {"type": "json_object"},
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a strict benchmark judge. "
                        "Evaluate continuity and erotic detail stability only. "
                        "Do not write prose outside JSON."
                    ),
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        }

    def judge(
        self,
        *,
        run_id: str,
        scenario,
        persona,
        transcript_payload: dict,
        rule_judge: JudgeResult,
    ) -> LLMJudgeResult:
        payload = json.dumps(
            self.build_request_payload(
                run_id=run_id,
                scenario=scenario,
                persona=persona,
                transcript_payload=transcript_payload,
                rule_judge=rule_judge,
            )
        ).encode("utf-8")
        request = urllib.request.Request(
            self.api_url,
            data=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.request_timeout_s) as response:
                response_payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:  # pragma: no cover - defensive
            raw = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"llm judge request failed: {raw[:500]}") from exc

        choice = (response_payload.get("choices") or [{}])[0]
        message = choice.get("message") or {}
        raw_content = message.get("content") or "{}"
        return parse_llm_judge_response(run_id=run_id, raw_response=raw_content)


def run_llm_judge(run_root: Path, rule_judge: JudgeResult) -> LLMJudgeResult:
    model_name = os.environ.get(JUDGE_LLM_MODEL_ENV)
    if not model_name:
        return LLMJudgeResult(
            run_id=rule_judge.run_id,
            relationship_continuity_score=0,
            erotic_detail_stability_score=0,
            assistantization_risk="none",
            detail_hollowing_risk="none",
            continuity_drift_risk="none",
            hard_break_confirmed=False,
            first_soft_degradation_turn=None,
            first_hard_break_turn=None,
            judge_labels=[],
            evidence=[],
            summary="LLM judge skipped because JUDGE_LLM_MODEL is not configured.",
            review_status="llm_judge_skipped",
        )

    metadata = json.loads((run_root / "metadata.json").read_text(encoding="utf-8"))
    transcript_payload = json.loads((run_root / "transcript.json").read_text(encoding="utf-8"))
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)
    persona = personas[(metadata["persona_id"], metadata["persona_version"])]
    scenario = scenarios[(metadata["scenario_id"], metadata["scenario_version"])]

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required when JUDGE_LLM_MODEL is set")
    api_url = os.environ.get("OPENAI_BASE_URL", DEFAULT_JUDGE_API_URL).rstrip("/")
    if not api_url.endswith("/chat/completions"):
        api_url = f"{api_url}/chat/completions"

    service = LLMJudgeService(
        model_name=model_name,
        api_key=api_key,
        api_url=api_url,
    )
    return service.judge(
        run_id=metadata["run_id"],
        scenario=scenario,
        persona=persona,
        transcript_payload=transcript_payload,
        rule_judge=rule_judge,
    )

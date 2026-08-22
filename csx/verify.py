"""The eval harness. Introduced in notebook 02, called at the end of every
notebook from 02 onward. This is what turns "I changed the instructions and
it feels better" into a pass/fail number.

Golden cases live in evals/golden_cases.json — one shared file, never
duplicated per-notebook. Each notebook may filter to the tags relevant to
what it just built (e.g. notebook 05 filters tags=["sharepoint"]) but it is
still the *same* case objects, so a regression anywhere shows up everywhere
downstream.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

GOLDEN_PATH = Path(__file__).resolve().parent.parent / "evals" / "golden_cases.json"


@dataclass
class CaseResult:
    case_id: str
    passed: bool
    latency_ms: float
    credits_delta: Optional[float]
    response_text: str
    reason: str = ""


@dataclass
class SuiteResult:
    results: list[CaseResult] = field(default_factory=list)

    @property
    def pass_rate(self) -> float:
        if not self.results:
            return 0.0
        return sum(r.passed for r in self.results) / len(self.results)

    @property
    def p50_latency_ms(self) -> float:
        if not self.results:
            return 0.0
        vals = sorted(r.latency_ms for r in self.results)
        return vals[len(vals) // 2]

    @property
    def total_credits(self) -> float:
        return sum(r.credits_delta or 0 for r in self.results)

    def report(self) -> str:
        lines = [f"{'PASS' if r.passed else 'FAIL':4}  {r.case_id:28}  {r.latency_ms:7.0f}ms  {r.reason}"
                 for r in self.results]
        lines.append("-" * 60)
        lines.append(
            f"pass_rate={self.pass_rate:.0%}  p50={self.p50_latency_ms:.0f}ms  "
            f"credits={self.total_credits:.2f}  n={len(self.results)}"
        )
        return "\n".join(lines)


def load_golden(tags: Optional[list[str]] = None, path: Path = GOLDEN_PATH) -> list[dict]:
    cases = json.loads(path.read_text())
    if tags:
        cases = [c for c in cases if set(c.get("tags", [])) & set(tags)]
    return cases


def _default_grader(case: dict, response_text: str) -> tuple[bool, str]:
    """Substring + citation-presence grading. Notebooks may pass a custom
    grader (e.g. branch-taken checks in 10, ontology-field checks in 17)."""
    expect = case.get("expect_contains", [])
    missing = [e for e in expect if e.lower() not in response_text.lower()]
    if missing:
        return False, f"missing expected terms: {missing}"

    if case.get("expect_citation") and "[1]" not in response_text and "http" not in response_text:
        return False, "expected a citation, none found"

    if case.get("expect_no_answer") and response_text.strip():
        # ungrounded-response policy cases: agent should decline, not hallucinate
        decline_markers = ["don't have", "do not have", "cannot find", "no information"]
        if not any(m in response_text.lower() for m in decline_markers):
            return False, "expected a decline, got a confident answer"

    return True, "ok"


def run_suite(
    client,
    cases: Optional[list[dict]] = None,
    tags: Optional[list[str]] = None,
    grader: Callable[[dict, str], tuple[bool, str]] = _default_grader,
    credit_meter=None,
    min_pass_rate: float = 0.8,
) -> SuiteResult:
    """Send every case's prompt to the published agent and grade the reply.

    Raises AssertionError if pass_rate < min_pass_rate — this is the gate,
    not just a report. A notebook that doesn't call run_suite (or doesn't
    check its result) has not verified anything.
    """
    cases = cases if cases is not None else load_golden(tags=tags)
    suite = SuiteResult()

    for case in cases:
        credits_before = credit_meter.snapshot() if credit_meter else None
        t0 = time.perf_counter()
        reply = client.ask_question(case["prompt"])  # microsoft_agents CopilotClient
        latency_ms = (time.perf_counter() - t0) * 1000
        text = getattr(reply, "text", str(reply))

        passed, reason = grader(case, text)
        credits_delta = (credit_meter.snapshot() - credits_before) if credit_meter else None

        suite.results.append(CaseResult(
            case_id=case["id"], passed=passed, latency_ms=latency_ms,
            credits_delta=credits_delta, response_text=text, reason=reason,
        ))

    print(suite.report())
    assert suite.pass_rate >= min_pass_rate, (
        f"eval gate failed: pass_rate={suite.pass_rate:.0%} < min_pass_rate={min_pass_rate:.0%}"
    )
    return suite

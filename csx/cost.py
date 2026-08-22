"""Credit accounting. Mandatory cost cell in every notebook — see finding #2:
the GHCP harness bills Copilot Credits from the moment you *build*, not just
when end users chat. Preview, test, and eval runs in these notebooks all
meter. A team that skips this file's output for 25 notebooks gets a
surprise invoice, not a POC.

This wraps the Power Platform analytics/admin surface. The exact endpoint
is admin-center analytics today; treat CreditMeter as the seam to swap in
the real client without touching every notebook's cost cell.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

LEDGER_PATH = Path(__file__).resolve().parent.parent / ".cost_ledger.jsonl"


@dataclass
class CreditMeter:
    environment_id: str
    _client: object = None  # lazily-built admin/analytics client

    def snapshot(self) -> float:
        """Current cumulative credits consumed by this environment's agents.

        Stubbed to read the last recorded ledger value in these notebooks —
        swap `_query_live()` in for a real tenant once notebook 00's admin
        checkpoint passes.
        """
        try:
            return self._query_live()
        except NotImplementedError:
            return self._last_ledger_value()

    def _query_live(self) -> float:
        raise NotImplementedError("Wire this to your tenant's Power Platform analytics API.")

    def _last_ledger_value(self) -> float:
        if not LEDGER_PATH.exists():
            return 0.0
        *_, last = LEDGER_PATH.read_text().splitlines() or [None]
        if last is None:
            return 0.0
        return json.loads(last)["cumulative_credits"]

    def record(self, notebook_id: str, delta_credits: float, note: str = "") -> None:
        cumulative = self._last_ledger_value() + delta_credits
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "notebook": notebook_id,
            "delta_credits": delta_credits,
            "cumulative_credits": cumulative,
            "note": note,
        }
        with LEDGER_PATH.open("a") as f:
            f.write(json.dumps(entry) + "\n")

    def report_cost(self, notebook_id: str, budget: int | None, delta_credits: float, note: str = "") -> None:
        self.record(notebook_id, delta_credits, note)
        cumulative = self._last_ledger_value()
        line = f"[{notebook_id}] +{delta_credits:.2f} credits this notebook, {cumulative:.2f} cumulative"
        if budget:
            pct = cumulative / budget * 100
            line += f"  ({pct:.1f}% of {budget}-credit budget)"
            if pct >= 90:
                print(f"⚠️  {line} — approaching budget, check with your admin before continuing")
                return
        print(line)

"""CLI entrypoint for the promotion gate used by infra/pipelines/deploy.yml.

    python -m csx.run_gate --tags core --min-pass-rate 0.8

Thin wrapper around csx.verify.run_suite so CI doesn't need a notebook
runtime — the same golden set and the same grader as the notebooks use
interactively, so a pass in CI means what a pass in `02` means.
"""
from __future__ import annotations

import argparse
import sys

from csx.clients import get_copilot_client
from csx.config import load_settings
from csx.cost import CreditMeter
from csx.verify import load_golden, run_suite


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tags", nargs="*", default=None)
    parser.add_argument("--min-pass-rate", type=float, default=0.8)
    args = parser.parse_args()

    settings = load_settings()
    client = get_copilot_client(settings, delegated=False)  # SP path — this is CI
    meter = CreditMeter(environment_id=settings.get("DATAVERSE_ENV_ID"))

    cases = load_golden(tags=args.tags)
    try:
        suite = run_suite(client, cases=cases, credit_meter=meter, min_pass_rate=args.min_pass_rate)
    except AssertionError as exc:
        print(f"GATE FAILED: {exc}", file=sys.stderr)
        return 1

    meter.report_cost("ci-gate", settings.get("COPILOT_CREDIT_BUDGET"), suite.total_credits)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

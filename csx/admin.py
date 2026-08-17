"""Tenant/admin prerequisite checks.

Several tracks (5, 6, 7) need switches a POC team may not control:
external-model enablement, preview-model enablement, cross-geo data
movement, cross-geo Fabric processing, environment-level OTel export.
Notebook 00 asserts every one of them up front and emits a single
prerequisite report so the team can raise one admin ticket instead of
discovering each switch mid-curriculum as a cryptic 403.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AdminSwitch:
    key: str
    surface: str          # PPAC / M365 admin center / Fabric admin portal
    setting: str
    required_by: list[str]  # notebook ids that need it
    status: bool | None = None  # None = unknown/unchecked


# The four independent model-availability switches from finding #5, plus
# the cross-geo / OTel switches from findings #11 and #13. These are
# declared, not queried automatically — PPAC/M365 admin API scopes vary by
# tenant, so notebook 00 has learners confirm each one against the portal
# and record it here, once, for the whole curriculum to trust.
REQUIRED_SWITCHES: list[AdminSwitch] = [
    AdminSwitch("external_models_ppac", "Power Platform admin center",
                "Environment/group setting: allow external (non-Microsoft) models",
                required_by=["22", "24"]),
    AdminSwitch("external_models_provider", "M365 admin center",
                "Per-provider approval (Anthropic / Mistral / xAI) — separate from the PPAC switch",
                required_by=["22", "24"]),
    AdminSwitch("preview_experimental_models", "Power Platform admin center",
                "Preview/experimental model enablement (distinct toggle from external models)",
                required_by=["22"]),
    AdminSwitch("move_data_across_regions", "Power Platform admin center",
                "Move data across regions — required for experimental models specifically",
                required_by=["22"]),
    AdminSwitch("fabric_cross_geo", "Fabric admin portal",
                "Cross-geo processing/storing tenant setting (Fabric IQ responses may leave the compliance boundary)",
                required_by=["16", "17"]),
    AdminSwitch("otel_span_export", "Power Platform admin center (environment level)",
                "Environment-level OpenTelemetry span export to Application Insights (PREVIEW since 15 Jul 2026)",
                required_by=["23"]),
]


def prerequisite_report(known_status: dict[str, bool]) -> str:
    """Render the one-ticket report. Pass in what notebook 00 learned by
    checking each switch against the live portal/API."""
    lines = ["Tenant/admin prerequisite report — raise ONE ticket covering all rows below:\n"]
    lines.append(f"{'switch':32} {'surface':32} {'status':8} needed by")
    for sw in REQUIRED_SWITCHES:
        status = known_status.get(sw.key)
        status_str = "OK" if status else ("MISSING" if status is False else "UNKNOWN")
        lines.append(f"{sw.key:32} {sw.surface:32} {status_str:8} notebooks {', '.join(sw.required_by)}")
    missing = [sw for sw in REQUIRED_SWITCHES if known_status.get(sw.key) is not True]
    if missing:
        lines.append(f"\n{len(missing)} switch(es) not yet confirmed on. Tracks 5/6/7 will fail fast, "
                      f"not weirdly, until these are set.")
    else:
        lines.append("\nAll switches confirmed. Tracks 5/6/7 are unblocked.")
    return "\n".join(lines)

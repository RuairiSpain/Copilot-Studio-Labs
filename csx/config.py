"""Environment/tenant configuration, loaded once and reused by every notebook.

Values come from a `.env` file at the repo root (never committed — see
.gitignore) or from real environment variables, which take precedence.
Nothing in this module talks to a network; it only resolves and validates
configuration, so `load_settings()` is safe to call at the top of every
notebook as the first "prereqs" cell.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

try:
    from dotenv import load_dotenv  # python-dotenv

    load_dotenv(REPO_ROOT / ".env", override=False)
except ImportError:  # pragma: no cover - dotenv is a dev convenience, not a hard dep
    pass

# Every var a notebook might need across the whole 00-25 arc. Individual
# notebooks only assert the subset they actually use — see csx.checkpoint.
_KNOWN_VARS = [
    "TENANT_ID",
    "DATAVERSE_ENV_ID",
    "DATAVERSE_ENV_URL",
    "PUBLISHER_PREFIX",
    "AGENT_SCHEMA_NAME",
    "APP_CLIENT_ID",          # confidential client / SP, application permission
    "APP_CLIENT_SECRET",
    "DELEGATED_CLIENT_ID",    # public client, delegated permission
    "AZURE_SUBSCRIPTION_ID",
    "AZURE_RESOURCE_GROUP",
    "AZURE_LOCATION",
    "AI_SEARCH_ENDPOINT",
    "AI_SEARCH_ADMIN_KEY",
    "STORAGE_ACCOUNT_NAME",
    "FOUNDRY_PROJECT_ENDPOINT",
    "FOUNDRY_IQ_KB_NAME",
    "SHAREPOINT_SITE_URL",
    "FABRIC_WORKSPACE_ID",
    "FABRIC_ONTOLOGY_ID",
    "APPINSIGHTS_CONNECTION_STRING",
    "COPILOT_CREDIT_BUDGET",  # integer, credits — set in notebook 00
]


@dataclass
class Settings:
    values: dict = field(default_factory=dict)

    def __getattr__(self, item):
        if item in self.values:
            return self.values[item]
        raise AttributeError(
            f"Settings has no '{item}'. Set it in .env or the environment, "
            f"then re-run load_settings()."
        )

    def get(self, key: str, default=None):
        return self.values.get(key, default)

    def require(self, *keys: str) -> None:
        """Fail fast, with a remediation hint, instead of a confusing 401 three cells later."""
        missing = [k for k in keys if not self.values.get(k)]
        if missing:
            raise EnvironmentError(
                "Missing required settings: "
                + ", ".join(missing)
                + ".\nSet these in a `.env` file at the repo root (see .env.example) "
                "or export them before starting Jupyter. Notebook 00 explains where "
                "each value comes from."
            )


def load_settings() -> Settings:
    values = {k: os.environ.get(k) for k in _KNOWN_VARS}
    budget = values.get("COPILOT_CREDIT_BUDGET")
    values["COPILOT_CREDIT_BUDGET"] = int(budget) if budget else None
    return Settings(values=values)

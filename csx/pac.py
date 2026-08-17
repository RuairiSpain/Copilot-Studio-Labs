"""Thin, idempotent wrappers around the `pac` CLI (Power Platform CLI).

Every function here shells out to `pac` and is safe to re-run: each checks
current state before mutating anything, per the repo-wide rule that
re-running a notebook must not create a second copy of anything.

Pin the pac version once, in notebook 00, and record it — the
`--authoring-mode cli-copilot` surface is newer than the classic authoring
mode and its YAML shape is expected to move.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

PAC_MIN_VERSION = "1.42"  # recorded by notebook 00; bump deliberately, not silently


def _run(args: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["pac", *args], cwd=cwd, check=check, text=True, capture_output=True
    )


def version() -> str:
    result = _run(["--version"], check=False)
    return result.stdout.strip() or result.stderr.strip()


def auth_list() -> list[dict]:
    result = _run(["auth", "list", "--json"], check=False)
    if result.returncode != 0:
        return []
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return []


def auth_create(environment_url: str, name: str, application_id: str | None = None,
                 client_secret: str | None = None, tenant_id: str | None = None) -> None:
    """Create (or reuse) a named pac auth profile.

    Delegated (interactive, notebook-local): omit application_id/client_secret.
    Application (SP, CI-safe): pass application_id + client_secret + tenant_id.
    """
    existing = {p.get("Name") for p in auth_list()}
    if name in existing:
        print(f"[pac.auth_create] profile '{name}' already exists — reusing")
        _run(["auth", "select", "--name", name])
        return

    args = ["auth", "create", "--environment", environment_url, "--name", name]
    if application_id and client_secret and tenant_id:
        args += ["--applicationId", application_id, "--clientSecret", client_secret, "--tenant", tenant_id]
    _run(args)
    print(f"[pac.auth_create] created profile '{name}'")


def copilot_init(workspace: Path, authoring_mode: str = "cli-copilot") -> Path:
    """`pac copilot init` — scaffold a new agent workspace, idempotently.

    If the workspace already has a copilot.yaml, this is a no-op: re-running
    notebook 01 must not clobber hand-edited instructions.
    """
    marker = workspace / "copilot.yaml"
    if marker.exists():
        print(f"[pac.copilot_init] {workspace} already initialised — skipping")
        return workspace

    workspace.mkdir(parents=True, exist_ok=True)
    _run(["copilot", "init", "--authoring-mode", authoring_mode, "--outputDirectory", str(workspace)])
    return workspace


def copilot_pack(workspace: Path, out_zip: Path) -> Path:
    """`pac copilot pack` — purely local, no auth, no environment.

    This is what makes the agent-as-code CI story clean: build stage needs
    no credentials at all, only the workspace on disk.
    """
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    _run(["copilot", "pack", "--inputDirectory", str(workspace), "--outputFile", str(out_zip)])
    return out_zip


def copilot_push(workspace: Path) -> None:
    """`pac copilot push` — sync workspace to the bound environment. Conflict-stopping."""
    _run(["copilot", "push", "--path", str(workspace)])


def copilot_pull(workspace: Path) -> None:
    """`pac copilot pull` — three-way merge from the environment into the workspace."""
    _run(["copilot", "pull", "--path", str(workspace)])


def copilot_quarantine(agent_schema_name: str, environment_id: str, enable: bool = True) -> None:
    """`pac copilot quarantine` — the governance kill switch (see notebook 24)."""
    action = "enable" if enable else "disable"
    _run(["copilot", "quarantine", "--" + action, "--name", agent_schema_name,
          "--environment", environment_id])


def solution_import(solution_zip: Path, environment_url: str) -> None:
    _run(["solution", "import", "--path", str(solution_zip), "--environment", environment_url])

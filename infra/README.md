# infra/ — the three IaC layers

See the root README for the full rationale. Short version:

| Layer | Path | Tool | Owns |
|---|---|---|---|
| Platform | `terraform/platform` | Terraform `microsoft/power-platform` | Dataverse environment, managed-environment settings, DLP, CI app admin, solution import |
| Agent | `../agents/contract-renewal-desk` | `pac copilot` | Instructions, knowledge refs, tools, skills, connection references, workflows |
| Azure deps | `bicep` | Bicep | AI Search, Storage, Foundry project + KB, App Insights, Key Vault |

`pipelines/` wires them together as build (agent-ci.yml, no auth) → deploy
(deploy.yml, SP auth + eval gate) → platform (platform-ci.yml, OIDC,
separate because it changes less often and needs a human approval gate on
prod).

**The one hard boundary, stated once here so no notebook has to pretend it
away:** connections and connection references are per-environment and
generally require interactive consent on first bind. IaC provisions the
*reference*; a human, or a pre-seeded service-principal connection, has to
satisfy it. `T1-bonus`, `T4-bonus`, and `T9-bonus` each hit this and each
say so explicitly.

Nothing here runs itself — every apply is triggered from a numbered
notebook (`T0-bonus` through `T9-bonus`) or from `Makefile`'s `plan`/`apply`
targets, and every apply is idempotent: re-running must not create a second
copy of anything.

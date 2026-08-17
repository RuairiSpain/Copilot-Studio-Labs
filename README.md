# Copilot Studio Enterprise Agent Curriculum

Twenty-six numbered notebooks plus ten bonus IaC notebooks, all evolving
**one** agent — the **Supplier Contract Renewal Desk** — from a hello-world
publish to a governed, observed, CI-promoted multi-agent fleet on Teams and
M365.

Doc alignment date: **17 Aug 2026**. Harness: **GitHub Copilot (GA 3 Aug
2026)**. Anything below marked `PREVIEW` is a surface that's moved recently
and may move again — treat it as such, not as settled ground.

## Read this before notebook `00`

Four decisions shape every notebook, no exceptions:

1. **Config-as-code, not click-throughs.** Notebooks emit or patch YAML in
   a `pac copilot` workspace and push it. Where a portal step is genuinely
   unavoidable, a **checkpoint cell** (`csx/checkpoint.py`) queries for the
   resulting object and raises loudly if it's missing — you cannot proceed
   on faith.
2. **One spine, evolved end to end.** `agents/contract-renewal-desk` is the
   only agent that matters from `01` to `25`; every notebook is a diff to
   it (see its `CHANGELOG.md`).
3. **The eval harness lands in `02`, not `23`.** `csx.verify.run_suite()`
   grades every notebook's published agent against the shared golden set in
   `evals/golden_cases.json`. Regression is visible, not assumed.
4. **The cost cell is mandatory.** The GHCP harness bills Copilot Credits
   from build time (see finding #2 below) — every notebook ends by
   recording what it spent, against the budget set in `00`.

Every notebook follows the same section order: **Goal → Prereqs (asserted
in code) → Concept → Build → Verify → Cost → Teardown.**

## What changed between the plan and this build (read this once)

Fourteen findings came out of the doc pass behind this curriculum. Six of
them invalidate parts of a naive first draft — know these before you start,
they explain design choices you'll otherwise find surprising.

| # | Finding | Where it shows up |
|---|---|---|
| 1 | Harness is chosen at agent creation and **cannot be changed** afterward. | `01` states this as the one irreversible decision in the curriculum. |
| 2 | GHCP **bills Copilot Credits from build time** — building, previewing, testing, and evaluating all meter. An M365 Copilot licence does not cover it. | `00` sets a real budget before anything is built; every notebook's Cost cell checks against it. |
| 3 | **Orchestration is not configurable** on GHCP — one enhanced orchestration model, every agent. | `02` is retitled around the levers that *do* exist: instructions, skill/tool/knowledge descriptions. |
| 4 | **Model is selected per agent, not per step.** | `22`'s cost tiering happens via connected agents, each pinned to its own model — never mid-agent. |
| 5 | External/preview models need **four independent admin switches** (PPAC env/group setting, M365 per-provider approval, preview/experimental toggle, cross-region data movement). | `00` and `22` both assert these before anything downstream depends on them. |
| 6 | **BYOM from Foundry is scoped to prompt tools** — never the agent's reasoning model. | `12` reframes "connect to Foundry" as "reach Foundry as a tool," explicitly. |
| 7 | **There is no native Azure Blob knowledge source.** | `04` is the two-hop lesson: Storage → AI Search indexer → attach as Azure AI Search. |
| 8 | `pac copilot pack` is **purely local — no auth, no environment.** | The build/deploy split in `infra/pipelines` — clean CI story. |
| 9 | Terraform `microsoft/power-platform` covers environments, DLP, solution import, with OIDC. | `infra/terraform/platform`, `T0-bonus`. |
| 10 | MCP is **Streamable HTTP only** (SSE retired Aug 2025) and rides connector infrastructure — DLP applies. | `13` proves DLP governs an MCP call, not just a demo connector. |
| 11 | Fabric responses **may leave the compliance boundary/geo** — needs F2+ capacity and a cross-geo tenant setting. | `16` leads with the compliance warning, not the demo. |
| 12 | Verify path needs `CopilotStudio.Copilots.Invoke`, delegated (local) or application/SP (CI). | `01` exercises both; `csx/clients.py` implements both. |
| 13 | Environment-level OTel export to App Insights is `PREVIEW`; a new **Agents (Preview)** view unifies Foundry + Copilot Studio traces. | `23` is stronger than a v1 plan would have had it — real spans, real KQL. |
| 14 | Power Platform API namespace moved to `copilotstudio`. | Any hand-rolled REST call in these notebooks uses the new namespace. |

## Repo layout

```
csx/          shared auth + clients + verify + cost + pac wrappers (notebooks stay thin)
agents/       pac copilot workspaces — contract-renewal-desk is the spine
apps/         canvas app workspace(s) — Part 2, optional elective (see below)
skills/       canonical SKILL.md bundles (from T2-bonus onward)
evals/        golden_cases.json — one shared set, every notebook, never duplicated
infra/
  terraform/  platform layer: environments, DLP, managed-environment settings
  bicep/      Azure layer: AI Search, Storage, Foundry, App Insights, Key Vault
  pipelines/  GitHub Actions — build (no auth) / deploy (SP + eval gate) / platform (OIDC)
notebooks/    00-25, plus T0-bonus … T9-bonus (core), 26-31 + T10-bonus (Part 2, optional)
Makefile      make verify | make golden | make plan | make apply | make teardown
```

Provisioning is idempotent throughout — re-running any notebook must not
create a second copy of anything. Every `Bicep`/`Terraform`/`pac` call in
this repo follows a get-or-create or declarative-diff pattern for that
reason.

## The three IaC layers

| Layer | Tool | Owns |
|---|---|---|
| Platform | Terraform `microsoft/power-platform` | Environments, managed-environment settings, DLP, CI app admin, solution import |
| Agent | `pac copilot` | Instructions, knowledge refs, tools, skills, connection references, workflows |
| Azure deps | Bicep | AI Search, Storage, Foundry project + KB, App Insights, Key Vault |

`pac copilot pack` needs no auth and no environment, so it runs in a build
stage; `pac solution import` (or `powerplatform_solution`) runs in a deploy
stage with OIDC. See `infra/README.md` for the one hard boundary this model
doesn't automate away: first-run connection consent is still a human (or a
pre-seeded SP connection) action, every time.

## Track structure

| Track | Notebooks | Theme |
|---|---|---|
| 0 — Foundations | `00`–`02`, `T0-bonus` | Environment, identity, credit budget, the eval harness |
| 1 — Knowledge | `03`–`06`, `T1-bonus` | Upload, Blob-via-AI-Search, SharePoint security trimming, recall/precision |
| 2 — Skills | `07`–`08`, `T2-bonus` | Token economics, routing bundles, selection failure modes |
| 3 — Workflows | `09`–`11`, `T3-bonus` | Deterministic steps, branching, variable-sourcing precedence |
| 4 — Foundry | `12`–`15`, `T4-bonus` | Foundry-as-tool, MCP, Foundry IQ KBs, serverless capstone |
| 5 — IQ surfaces | `16`–`19`, `T5-bonus` | Fabric IQ, Work IQ, Web IQ — compliance and consent boundaries |
| 6 — Multi-agent | `20`–`22`, `T6-bonus` | Connected agents, loops/graphs, per-tier model economics |
| 7 — Observability | `23`, `T7-bonus` | OTel spans, App Insights, deterministic replay |
| 8 — Governance | `24`, `T8-bonus` | DLP, quarantine, guard tests that fail when the guard is removed |
| 9 — Production | `25`, `T9-bonus` | ALM, promotion gates, a deliberate bad deploy and its recovery |

## Part 2 — Power Platform app development (optional elective)

Notebooks `26`–`31` plus `T10-bonus`. **Nothing in `00`–`25` or
`T0`–`T9-bonus` depends on this track** — it's for instructors who want to
extend the workshop past "agent alone" into "agent embedded in a
traditional Power Platform app," using the same spine scenario, the same
Dataverse environment, and the same `crd_contract-renewal-desk` agent.

| Notebook | Theme |
|---|---|
| `26` | Data modeling on Dataverse — the tables `09`–`17`'s workflows/MCP tools assumed existed, made real, plus two security roles |
| `27` | Canvas app fundamentals — browse/detail screens, via Power Platform Git Integration |
| `28` | Embedding the agent as a control — the actual "agent inside an app" lab |
| `29` | Power Automate flow fundamentals — Dataverse-trigger and button-triggered flows |
| `30` | Agent-as-a-flow-step — the automation-surface complement to `28`'s chat surface |
| `31` | Capstone: app → flow → agent → Dataverse write-back → app reflects the change, security-role boundary proven end to end |
| `T10-bonus` | Extends `T9-bonus`'s CI/CD pipeline to gate on the app + its flows, not just the agent |

**Two findings from this track's own doc pass (checked 17 Aug 2026), because
both invalidate the obvious first approach:**

| # | Finding | Impact |
|---|---|---|
| P1 | `pac canvas pack`/`unpack` is **deprecated**. Power Platform **Git Integration (GA)** is the supported path for canvas app source control — bind an environment to a repo, and every designer save syncs unpacked YAML back automatically. | `27` uses Git Integration as the primary mechanism; `csx.pac.canvas_pack`/`canvas_unpack` are kept only for narrow CI-side scripted diffing, explicitly flagged deprecated in their docstrings. |
| P2 | The native **"Add AI Copilot" canvas control was deprecated 2 Feb 2026** — it can no longer be added to a new canvas app. | `28` embeds the agent via the community **ChatControl PCF** (Bot Framework WebChat, imported as a solution) instead, and calls out Microsoft's longer-term direction (M365 Copilot in canvas apps, still preview) as something to re-check before teaching this notebook again. |

Flows don't get their own authoring CLI either — `pac solution unpack`
is the mechanism (`29`), the same idea as `agents/`'s YAML, applied to a
solution's `Workflows`/cloud-flow JSON instead of a `copilot.yaml`.

## Sequencing note

Tracks 5, 6, and 7 each depend on tenant-level admin switches a POC team
may not control. Run `00`'s prerequisite-report cell first — it lists every
switch the full curriculum needs so you raise **one** ticket, not nine.

## Open risks

- Roughly a quarter of this curriculum sits on `PREVIEW` surfaces: Foundry
  IQ Serverless (`15`), Fabric IQ Ontology + MCP (`17`), environment-level
  OTel export (`23`), the App Insights Agents view (`23`). Expect drift.
- Credit consumption during authoring is real — `25` in particular (a full
  promotion plus a deliberate bad deploy and recovery) is the most
  expensive single notebook. Model per-learner cost before a group rollout.
- `pac copilot`'s `cli-copilot` authoring mode is newer than classic
  authoring; its YAML schema is more likely to move than the rest of the
  CLI surface. `00` pins the exact `pac` version validated against this
  curriculum — bump it deliberately, not silently.
- Part 2's `28` builds on the community **ChatControl PCF** sample, not a
  first-party control — it's the correct current answer only because the
  native control was deprecated 2 Feb 2026 and Microsoft's replacement
  (M365 Copilot in canvas apps) is still preview. Re-verify before each
  cohort; this is the single most likely thing in the whole repo to have
  moved again by the time you teach it.

## Getting started

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in per notebooks/00's explanations
jupyter lab notebooks/00_environment_identity_credit_meter.ipynb
```

Then work numerically, `00` → `25`, running each track's bonus notebook
whenever you want the IaC-reproducible version of what the numbered
notebook just did interactively. Continue into `26` → `31` (+ `T10-bonus`)
only if your cohort wants the Power Platform app-development elective —
skip straight to wrap-up otherwise.

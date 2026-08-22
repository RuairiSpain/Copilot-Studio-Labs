# Contract Renewal Desk — changelog

One spine agent, evolved end to end. Every row is one notebook's diff to
this workspace. If `git log -p agents/contract-renewal-desk` disagrees with
this table, trust git — update this table.

| Notebook | Adds |
|---|---|
| `01` | Agent created: `copilot.yaml`, empty `instructions.md`, harness=github-copilot chosen (irreversible), published, invoked, deleted (throwaway hello-world instance — the spine instance is created fresh in `02`) |
| `02` | Real `instructions.md`; `evals/golden_cases.json` 12-case core set; first `run_suite()` gate |
| `03` | `knowledge/meridian-msa.pdf` source (native upload) |
| `04` | `knowledge/addenda-search-index` source (Azure AI Search over blob-indexed scans) |
| `05` | `knowledge/supplier-contracts-sharepoint` source (SharePoint, security-trimmed) |
| `06` | Knowledge source `description` fields tuned for selection at scale; ungrounded-response policy set |
| `07` | (no knowledge/instruction change — token-accounting comparison only) |
| `08` | `skills/renewal-routing/SKILL.md` + 3 sub-skills |
| `09` | `workflows/renewal-check.yaml` (linear) |
| `10` | `workflows/renewal-check.yaml` gains If/Else + human-review step |
| `11` | `workflows/renewal-check.yaml` variable sourcing hardened (empty-variable guard) |
| `12` | `mcpServers` unchanged; adds a **prompt tool** backed by a Foundry-deployed extraction model |
| `13` | `mcpServers: [finance-ops-mcp]` (Streamable HTTP, on-behalf-of auth) |
| `14` | `knowledge/foundry-iq-supplier-risk` source |
| `15` | `knowledge/foundry-iq-serverless-capstone` source (compared against `03`-`05` on the same eval set, then removed to keep the spine agent's cost profile stable) |
| `16` | `knowledge/fabric-spend-semantic-model` source |
| `17` | `mcpServers` gains `fabric-iq-ontology-mcp` |
| `18` | Work IQ enabled (tenant-level; no workspace diff, consent boundary documented in the notebook) |
| `19` | Web IQ enabled (tenant-level; no workspace diff, injection defence added to `instructions.md`) |
| `20` | `connectedAgents: [drafting-specialist]` |
| `21` | `connectedAgents` gains `critic-reviewer` (loop) and fan-out graph wiring |
| `22` | `connectedAgents` re-pinned per tier: `extraction-agent` (cheap), `routing-agent` (mid), `drafting-specialist` (frontier) |
| `23` | Environment-level OTel export enabled (tenant-level; no workspace diff) |
| `24` | DLP/quarantine/content-safety settings; guard tests added to `evals/` |
| `25` | Solution-packaged, promoted dev → test → prod, published to Teams |

Bonus tracks (`T0`–`T9`) parallel this table in `infra/` and `.github/workflows/`
rather than in this workspace — they provision what this table assumes
already exists (the Dataverse environment, the Azure dependencies, the CI
pipeline) rather than changing the agent itself.

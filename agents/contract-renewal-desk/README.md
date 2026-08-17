# agents/contract-renewal-desk

This is the `pac copilot` workspace for the curriculum's single spine agent
— the **Supplier Contract Renewal Desk**. Every notebook from `01` to `25`
adds one capability here; nothing is a disconnected toy.

```
copilot.yaml     agent manifest — harness, model, publisher, source lists
instructions.md  the only orchestration lever on the GHCP harness (finding #3)
knowledge/       knowledge-source definitions (populated 03-06, 14-15)
skills/          SKILL.md bundles (populated 07-08)
workflows/       workflow YAML (populated 09-11)
CHANGELOG.md     which notebook added what — read this before diffing
```

## Working with this workspace

```bash
pac copilot pull  --path agents/contract-renewal-desk   # three-way merge from the environment
pac copilot pack  --inputDirectory agents/contract-renewal-desk --outputFile dist/crd.zip  # no auth needed
pac copilot push  --path agents/contract-renewal-desk   # conflict-stopping push
```

`pac copilot pack` needs no auth and no environment — that's what keeps the
CI build stage clean (see `infra/pipelines` and `T9-bonus`).

## Do not hand-edit around a checkpoint

If a notebook's checkpoint cell says a portal step is required (first-run
connection consent, some connection-reference binding), do that step, don't
work around it by hand-editing YAML the harness would reject anyway — the
checkpoint exists because the object genuinely can't be created any other
way today.

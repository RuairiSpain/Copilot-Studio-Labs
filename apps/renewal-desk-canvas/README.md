# apps/renewal-desk-canvas

The companion canvas app for **Part 2** of the curriculum (`notebooks/26`–`31`,
`T10-bonus`) — a procurement rep's working surface over the same Dataverse
tables and the same agent (`crd_contract-renewal-desk`) that Part 1 builds.
Part 2 is an **optional elective track**; nothing in `notebooks/00`–`25` or
`T0`–`T9-bonus` depends on this directory existing.

```
src/            Git-Integration-synced canvas app source (YAML per screen/control)
flows/          unpacked Power Automate flow definitions (pac solution unpack output)
CHANGELOG.md    which notebook added what — same convention as agents/contract-renewal-desk
```

## Why this isn't authored the way `agents/` is

`agents/contract-renewal-desk` is `pac copilot`-native — the whole workspace
is hand-editable YAML. A canvas app is a WYSIWYG-authored artifact; there is
no equivalent "just write YAML by hand and it works" path. What *does* exist,
and what this app uses:

- **Power Platform Git Integration (GA)** — bind the environment to this
  repo, and every save in the canvas app designer syncs the unpacked
  YAML/JSON source under `src/` back here automatically. This is the
  primary mechanism, not `pac canvas pack`/`unpack` (deprecated — still
  callable, but Microsoft's own guidance now points at Git Integration).
- **`pac solution unpack`** for the flows under `flows/` — cloud flows in a
  solution unpack to per-flow JSON under a `modernflows/` folder; that JSON
  is what this repo actually diffs and reviews.

Screens and controls are still built in the canvas app designer — that's a
`checkpoint()` cell in `27`/`28`, not a workaround. What's config-as-code
here is everything *after* that first WYSIWYG pass: the synced source is
what you diff, review, and promote.

## Source-of-truth note

The files under `src/` and `flows/` in this initial commit are
**representative placeholders**, not a real Git-Integration sync — they
show the shape notebook `27` onward will overwrite once you've bound a real
environment. Don't hand-edit them expecting the designer to pick up your
changes; let Git Integration regenerate them, the same caution
`agents/contract-renewal-desk/README.md` gives for checkpoint-gated steps.

# evals/

One golden set, `golden_cases.json`, shared by every notebook from `02` on.
Never fork or duplicate cases per-notebook — if you need a new one, add it
here with tags, and filter by tag in the notebook that needs it.

## Shape

```json
{
  "id": "unique-stable-id",
  "tags": ["core", "knowledge", "..."],
  "prompt": "what the eval sends the agent",
  "expect_contains": ["substrings the response must contain, case-insensitive"],
  "expect_citation": false,
  "expect_no_answer": false,
  "run_as": "optional persona — used by 05's security-trimming pair"
}
```

`csx.verify.run_suite()` grades with the default substring/citation grader.
Notebooks that need custom grading (branch-taken checks in `10`, ontology
field checks in `17`, tier-selection checks in `22`) pass their own
`grader(case, response_text) -> (bool, reason)`.

## Tag map (which notebook filters which tags)

| Tags | Introduced/used by |
|---|---|
| `core` | `02` (the base 12-case set), every notebook thereafter as a regression floor |
| `knowledge`, `blob`, `sharepoint`, `security-trimming`, `ungrounded`, `recall`, `precision` | `03`–`06` |
| `workflow`, `branch-renew`, `branch-escalate`, `empty-variable`, `human-review` | `09`–`11` |
| `foundry`, `mcp`, `foundry-iq` | `12`–`15` |
| `fabric`, `fabric-iq`, `ontology`, `workiq`, `pii`, `webiq`, `injection` | `16`–`19` |
| `multi-agent`, `model-tier`, `extraction`, `routing` | `20`–`22` |
| `governance`, `dlp`, `secrets`, `content-safety` | `24` |

## Growing the set

Golden cases are cheap to add and expensive to remove — removing one erases
a regression signal permanently. If a case stops being relevant (e.g. a
supplier is retired from the spine scenario), retag it rather than delete
it, unless it is provably redundant with another case.

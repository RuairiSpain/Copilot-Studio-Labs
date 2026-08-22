# apps/renewal-desk-canvas — changelog

| Notebook | Adds |
|---|---|
| `26` | Dataverse tables the app and agent both use: `crd_supplierspend`, `crd_supplierperformance`, `crd_supplierrenewal` — columns, relationships, two security roles (`Procurement Lead`, `Procurement Analyst`) |
| `27` | `src/`: environment bound to Git Integration; `SupplierBrowse` (gallery) and `SupplierDetail` (form) screens |
| `28` | `src/Screens/SupplierDetail`: ChatControl PCF added, configured against `crd_contract-renewal-desk`, wired to pass the selected supplier as chat context |
| `29` | `flows/`: `NotifyOnHighRiskFlag` (Dataverse-trigger flow), `TriageOnDemand` (button-triggered from the app) |
| `30` | `flows/TriageOnDemand`: calls the agent's API directly (agent-as-a-step), posts a Teams message |
| `31` | `flows/TriageOnDemand`: writes the agent's structured response back to `crd_supplierrenewal`; `SupplierDetail` screen refreshes from the write; security-role-scoped verification added |

Bonus (`T10-bonus`) parallels this table in `infra/pipelines` rather than
changing this workspace — it wires the Git-Integration-synced source and
the unpacked flow JSON into the same CI/CD pipeline `T9-bonus` built for
the agent fleet.

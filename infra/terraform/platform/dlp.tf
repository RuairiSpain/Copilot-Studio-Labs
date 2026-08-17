# T8-bonus — policy as code. A DLP policy that governs both connectors and
# MCP servers (MCP rides connector infrastructure — finding #10 — so this
# one policy covers both, not a separate MCP allowlist).
#
# Kept minimal and workshop-scoped: Business = data sources the spine agent
# actually uses (Dataverse, SharePoint, Azure AI Search, the finance MCP
# connector); everything else defaults to Blocked. Loosen deliberately, not
# by omission.

resource "powerplatform_data_loss_prevention_policy" "contract_renewal_desk" {
  display_name              = var.dlp_policy_name
  default_connectors_classification = "Blocked"
  environment_type           = "OnlyEnvironments"
  environments                = [powerplatform_environment.this.id]

  business_connectors = [
    "/providers/Microsoft.PowerApps/apis/shared_commondataserviceforapps", # Dataverse
    "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
    "/providers/Microsoft.PowerApps/apis/shared_cognitiveservicesazuresearch", # Azure AI Search
  ]

  non_business_connectors = []
  blocked_connectors      = []

  # See notebooks/24: a guard with no test is a comment pretending to be a
  # control. csx/verify.py's governance-tagged cases assert the finance MCP
  # connector is reachable and everything else is not, on every run.
}

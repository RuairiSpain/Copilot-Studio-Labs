// notebooks/12-15 — Foundry project used two ways in this curriculum:
//   1. A cheap model deployment reached from the agent as a *tool*
//      (prompt tool / workflow AI action / Function-wrapped endpoint —
//      finding #6, never the agent's reasoning model).
//   2. A Foundry IQ knowledge base (notebooks/14) and its serverless
//      variant (notebooks/15, PREVIEW).

param namePrefix string
param location string

resource foundryAccount 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: take('${namePrefix}-foundry', 64)
  location: location
  kind: 'AIServices'
  sku: { name: 'S0' }
  properties: {
    customSubDomainName: take('${namePrefix}-foundry', 64)
    publicNetworkAccess: 'Enabled'
  }
}

resource extractionModelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = {
  parent: foundryAccount
  name: 'extraction-mini'
  sku: {
    name: 'Standard'
    capacity: 10
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: 'gpt-4o-mini'
      version: '2024-07-18'
    }
  }
}

output projectEndpoint string = foundryAccount.properties.endpoint
output extractionDeploymentName string = extractionModelDeployment.name

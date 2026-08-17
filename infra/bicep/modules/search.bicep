// notebooks/04 — Azure AI Search is the knowledge source Copilot Studio
// actually supports (finding #7). The indexer + skillset that reads the
// blob container are created by the notebook via the Search REST/SDK, not
// here, because they reference the storage connection string produced by
// this same deployment — sequencing that's clearer as notebook code than
// as Bicep-on-Bicep.

param namePrefix string
param location string
param sku string = 'basic'

resource search 'Microsoft.Search/searchServices@2024-06-01-preview' = {
  name: take('${namePrefix}-search', 60)
  location: location
  sku: { name: sku }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
    publicNetworkAccess: 'enabled' // tighten to 'disabled' + private endpoint for prod, see notebooks/24
  }
}

output endpoint string = 'https://${search.name}.search.windows.net'
output adminKey string = search.listAdminKeys().primaryKey

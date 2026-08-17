// Secrets (AI Search admin key, storage connection string, MCP endpoint
// secrets for notebooks/13) live here, referenced by the agent workspace
// via connection reference rather than inlined into copilot.yaml or any
// notebook — see notebooks/24's secret-handling section.

param namePrefix string
param location string

@secure()
param secrets object

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: take('${namePrefix}-kv', 24)
  location: location
  properties: {
    sku: { family: 'A', name: 'standard' }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    enableSoftDelete: true
  }
}

resource aiSearchAdminKeySecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'ai-search-admin-key'
  properties: {
    value: secrets.aiSearchAdminKey
  }
}

resource storageConnectionStringSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'storage-connection-string'
  properties: {
    value: secrets.storageConnectionString
  }
}

output vaultUri string = keyVault.properties.vaultUri

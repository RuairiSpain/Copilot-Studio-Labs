// Azure dependency layer (see repo README "IaC model"). Owns AI Search,
// Storage, Foundry project + KB, App Insights, Key Vault — everything the
// spine agent reaches as a *tool* or knowledge backend, never the agent
// definition itself (that's agents/contract-renewal-desk via `pac copilot`).
//
// Idempotent: `az deployment group create` re-run with the same params must
// not create duplicate resources — Bicep's declarative model gives this for
// free as long as resource names are deterministic, which is why every
// module below derives its name from `namePrefix` rather than a generated
// GUID.

targetScope = 'resourceGroup'

@description('Short, deterministic prefix for all resource names, e.g. crd-dev')
param namePrefix string

@description('Azure region for all resources')
param location string = resourceGroup().location

@description('AI Search SKU. basic is enough for the workshop corpus in notebooks/04')
param searchSku string = 'basic'

module storage 'modules/storage.bicep' = {
  name: 'storage'
  params: {
    namePrefix: namePrefix
    location: location
  }
}

module search 'modules/search.bicep' = {
  name: 'search'
  params: {
    namePrefix: namePrefix
    location: location
    sku: searchSku
  }
}

module foundry 'modules/foundry.bicep' = {
  name: 'foundry'
  params: {
    namePrefix: namePrefix
    location: location
  }
}

module appInsights 'modules/appinsights.bicep' = {
  name: 'appinsights'
  params: {
    namePrefix: namePrefix
    location: location
  }
}

module keyVault 'modules/keyvault.bicep' = {
  name: 'keyvault'
  params: {
    namePrefix: namePrefix
    location: location
    secrets: {
      aiSearchAdminKey: search.outputs.adminKey
      storageConnectionString: storage.outputs.connectionString
    }
  }
}

output storageAccountName string = storage.outputs.accountName
output searchEndpoint string = search.outputs.endpoint
output foundryProjectEndpoint string = foundry.outputs.projectEndpoint
output appInsightsConnectionString string = appInsights.outputs.connectionString
output keyVaultUri string = keyVault.outputs.vaultUri

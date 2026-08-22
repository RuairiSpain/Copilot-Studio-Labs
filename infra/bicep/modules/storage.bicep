// notebooks/04 — blob container for scanned addenda. There is no native
// Azure Blob knowledge source in Copilot Studio (finding #7); this account
// exists purely to be indexed by modules/search.bicep's indexer, which is
// the two-hop shape that notebook attaches as "Azure AI Search" knowledge.

param namePrefix string
param location string

var accountName = replace('${namePrefix}addenda', '-', '')

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: take(accountName, 24)
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = {
  parent: storage
  name: 'default'
}

resource addendaContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  parent: blobService
  name: 'supplier-addenda'
  properties: {
    publicAccess: 'None'
  }
}

output accountName string = storage.name
output connectionString string = 'DefaultEndpointsProtocol=https;AccountName=${storage.name};AccountKey=${storage.listKeys().keys[0].value};EndpointSuffix=core.windows.net'

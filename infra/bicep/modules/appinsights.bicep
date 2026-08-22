// notebooks/23 — the destination for environment-level OTel span export
// (PREVIEW toggle, set at the Power Platform environment level, not here).
// This module only creates the App Insights resource + workspace; the
// export toggle itself is a PPAC setting the notebook flips and checkpoints.

param namePrefix string
param location string

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: take('${namePrefix}-logs', 63)
  location: location
  properties: {
    sku: { name: 'PerGB2018' }
    retentionInDays: 30
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: take('${namePrefix}-appi', 63)
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
    IngestionMode: 'LogAnalytics'
  }
}

output connectionString string = appInsights.properties.ConnectionString
output workspaceId string = logAnalytics.id

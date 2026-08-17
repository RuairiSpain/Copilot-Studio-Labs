terraform {
  required_version = ">= 1.8.0"

  required_providers {
    powerplatform = {
      source  = "microsoft/power-platform"
      version = "~> 3.0"
    }
  }

  # Remote state — fill in for your tenant. Kept as a stub so this repo
  # doesn't assume a specific backend; T0-bonus documents choosing one.
  backend "azurerm" {
    # resource_group_name  = "rg-copilot-studio-labs-tfstate"
    # storage_account_name = "<globally-unique>"
    # container_name       = "tfstate"
    # key                  = "platform.tfstate"
  }
}

# OIDC federated credential auth for CI (finding #9) — no long-lived secret
# in the pipeline. Interactive `az login` / `pac auth create` is fine for
# T0-bonus's local `terraform apply`; the pipeline in infra/pipelines uses
# this block via env vars ARM_USE_OIDC / ARM_CLIENT_ID / ARM_TENANT_ID /
# ARM_SUBSCRIPTION_ID.
provider "powerplatform" {
  use_oidc = true
}

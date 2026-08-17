# Platform layer (see repo README "IaC model"): environments, managed
# environment settings, Copilot Studio environment settings, DLP, app users.
# Does NOT own the agent itself — that's agents/contract-renewal-desk via
# `pac copilot`. Does NOT own Azure dependencies — that's infra/bicep.
#
# Idempotent by construction: `terraform plan` after a no-op change should
# show zero diffs. Re-running `terraform apply` must never create a second
# environment — that's what makes T0-bonus's teardown drill trustworthy.

resource "powerplatform_environment" "this" {
  display_name     = var.environment_display_name
  location         = var.location
  environment_type = var.environment_type

  dataverse = {
    language_code     = "1033"
    currency_code     = "USD"
    security_group_id = null # open to the whole tenant for the workshop; scope this in prod
  }
}

resource "powerplatform_managed_environment" "this" {
  count          = var.is_managed_environment ? 1 : 0
  environment_id = powerplatform_environment.this.id

  is_group_sharing_disabled      = false
  limit_sharing_mode             = var.copilot_limit_sharing_mode
  max_limit_user_sharing         = var.copilot_max_limit_user_sharing
  is_usage_insights_disabled     = false
  is_ai_generative_settings_open = true # Copilot Studio features on
}

# Copilot Studio-specific environment settings (feature toggles + the
# credit/agent-limit posture set in notebooks/00, before anything is built —
# finding #2).
resource "powerplatform_environment_settings" "this" {
  environment_id = powerplatform_environment.this.id

  product = {
    behavior_settings = {
      show_dashboard_cards_for_environment_maker = true
    }
  }
}

# Grants the CI service principal System Administrator on the environment so
# `pac copilot push` / `pac solution import` in infra/pipelines can run
# unattended (application permission path — see csx/clients.py).
resource "powerplatform_environment_application_admin" "ci" {
  environment_id = powerplatform_environment.this.id
  application_id = var.admin_app_object_id
}

output "environment_id" {
  value = powerplatform_environment.this.id
}

output "environment_url" {
  value = powerplatform_environment.this.dataverse.url
}

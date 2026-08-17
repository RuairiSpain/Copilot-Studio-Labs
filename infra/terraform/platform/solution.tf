# T9-bonus — deploy stage. Imports the solution zip that the build stage
# produced with `pac copilot pack` (no auth needed for pack — see
# infra/pipelines/agent-ci.yml). This resource is the Terraform-native
# alternative to a `pac solution import` pipeline step; either works, this
# repo's pipeline uses `pac solution import` directly and keeps this file
# as the documented alternative for teams standardised on Terraform for
# every deploy action.

variable "solution_zip_path" {
  description = "Path to the packed solution zip (dist/crd.zip), produced by the build stage"
  type        = string
  default     = null
}

resource "powerplatform_solution" "contract_renewal_desk" {
  count           = var.solution_zip_path == null ? 0 : 1
  environment_id  = powerplatform_environment.this.id
  solution_file   = var.solution_zip_path
  solution_name   = "crd_contract-renewal-desk"
}

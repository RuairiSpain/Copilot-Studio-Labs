variable "environment_display_name" {
  description = "Dataverse/Power Platform environment display name, e.g. 'Contract Renewal Desk - dev'"
  type        = string
}

variable "environment_type" {
  description = "Sandbox | Production | Trial — sandbox for dev/test, Production for the ALM target (notebooks/25)"
  type        = string
  default     = "Sandbox"
}

variable "location" {
  description = "Power Platform region, e.g. unitedstates, europe"
  type        = string
}

variable "is_managed_environment" {
  description = "Whether to layer Managed Environment governance on top (notebooks/24)"
  type        = bool
  default     = true
}

variable "copilot_limit_sharing_mode" {
  description = "Managed-environment agent sharing limit mode (T8-bonus). 'ExcludeSharingToSecurityGroups' | 'NoLimit'"
  type        = string
  default     = "ExcludeSharingToSecurityGroups"
}

variable "copilot_max_limit_user_sharing" {
  description = "Max users an unmanaged agent share can reach, when sharing mode limits it"
  type        = number
  default     = 10
}

variable "admin_app_object_id" {
  description = "Object ID of the service principal granted System Administrator on the environment (for CI to run pac copilot push / solution import unattended)"
  type        = string
}

variable "dlp_policy_name" {
  description = "Name of the DLP policy created/attached for this environment (T8-bonus)"
  type        = string
  default     = "contract-renewal-desk-dlp"
}

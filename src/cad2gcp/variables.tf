variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"      # it’s fine to leave non-secret defaults
}

variable "billing_account_id" {
  description = "GCP Billing Account ID"
  type        = string
}

variable "budget_display_name" {
  description = "Display name of the Budget"
  type        = string
}

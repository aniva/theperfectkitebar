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

variable "bucket_name" {
  description = "Name of the GCS bucket to revoke allUsers from"
  type        = string
}

variable "pubsub_topic" {
  description = "Full Pub/Sub topic path for budget alerts, e.g. projects/your-project/topics/alerts"
  type        = string
}

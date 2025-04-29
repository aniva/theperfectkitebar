provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "cad_assets" {
  name          = "theperfectkitebar-CAD-assets"
  location      = var.region
  force_destroy = true
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_iam_binding" "public_access" {
  bucket = google_storage_bucket.cad_assets.name
  role   = "roles/storage.objectViewer"
  members = ["allUsers"]
}

resource "google_pubsub_topic" "budget_alerts" {
  name = "cad-budget-alerts"
}

resource "google_storage_bucket_object" "shapr_placeholder" {
  name   = "hardware/.keep"
  bucket = google_storage_bucket.cad_assets.name
  content = ""
}

resource "google_cloudfunctions_function" "disable_access" {
  name        = "disablePublicAccess"
  description = "Disables public access to GCS bucket if budget exceeded"
  runtime     = "python310"
  region      = var.region
  source_archive_bucket = google_storage_bucket.cad_assets.name
  source_archive_object = "functions.zip"
  entry_point = "disable_bucket_public_access"
  trigger_topic = google_pubsub_topic.budget_alerts.name

  available_memory_mb   = 128
  timeout               = 60
}

resource "google_storage_bucket_object" "function_zip" {
  name   = "functions.zip"
  bucket = google_storage_bucket.cad_assets.name
  source = "${path.module}/functions.zip"
}

# main.tf (updated with separate fn_code bucket for function zips)

provider "google" {
  project = var.project_id
  region  = var.region
}

# === CAD Asset Bucket (public, serves STL etc.) ===
resource "google_storage_bucket" "cad_assets" {
  name                        = "theperfectkitebar-cad-assets"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_iam_binding" "public_access" {
  bucket = google_storage_bucket.cad_assets.name
  role   = "roles/storage.objectViewer"
  members = ["allUsers"]
}

# === Separate Function Code Bucket (private) ===
resource "google_storage_bucket" "fn_code" {
  name                        = "theperfectkitebar-fn-code"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_iam_binding" "fn_code_private" {
  bucket = google_storage_bucket.fn_code.name
  role   = "roles/storage.objectViewer"
  members = [
    "projectOwner:${var.project_id}",
    "projectEditor:${var.project_id}"
  ]
}

# === Pub/Sub Topic for Budget Alerts ===
resource "google_pubsub_topic" "budget_alerts" {
  name = "cad-budget-alerts"
}

# === Function Zip Files ===
resource "google_storage_bucket_object" "function_zip" {
  name   = "functions.zip"
  bucket = google_storage_bucket.fn_code.name
  source = "${path.module}/functions.zip"
}

resource "google_storage_bucket_object" "function_zip_enable" {
  name   = "functions-enable.zip"
  bucket = google_storage_bucket.fn_code.name
  source = "${path.module}/functions-enable.zip"
}

# === .keep placeholder to persist hardware/ ===
resource "google_storage_bucket_object" "shapr_placeholder" {
  name    = "hardware/.keep"
  bucket  = google_storage_bucket.cad_assets.name
  content = "placeholder"
}

# === Disable Function ===
resource "google_cloudfunctions_function" "disable_access" {
  name                  = "disablePublicAccess"
  description           = "Disables public access to GCS bucket if budget exceeded"
  runtime               = "python310"
  region                = var.region
  available_memory_mb   = 128
  timeout               = 60
  entry_point           = "disable_bucket_public_access"
  source_archive_bucket = google_storage_bucket.fn_code.name
  source_archive_object = google_storage_bucket_object.function_zip.name

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.budget_alerts.id
  }
}

# === Enable Function ===
resource "google_cloudfunctions_function" "enable_access" {
  name                  = "enablePublicAccess"
  description           = "Re-enables public access on 1st of the month"
  runtime               = "python310"
  region                = var.region
  available_memory_mb   = 128
  timeout               = 60
  entry_point           = "enable_bucket_public_access"
  trigger_http          = true
  source_archive_bucket = google_storage_bucket.fn_code.name
  source_archive_object = google_storage_bucket_object.function_zip_enable.name
}

# === Monthly Re-enable Access Job ===
resource "google_cloud_scheduler_job" "monthly_reenable_access" {
  name             = "reenable-public-access"
  description      = "Re-enable public GCS access monthly"
  schedule         = "0 0 1 * *"
  time_zone        = "America/Toronto"
  attempt_deadline = "60s"

  http_target {
    http_method = "POST"
    uri         = google_cloudfunctions_function.enable_access.https_trigger_url
    oidc_token {
      service_account_email = google_cloudfunctions_function.enable_access.service_account_email
    }
  }

  region  = var.region
  project = var.project_id
}

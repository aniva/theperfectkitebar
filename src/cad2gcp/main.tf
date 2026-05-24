terraform {
  required_providers {
    archive = {
      source  = "hashicorp/archive"
      version = ">= 2.4.0"
    }
    google = {
      source  = "hashicorp/google"
      version = ">= 6.33.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# === Enable Required APIs ===
resource "google_project_service" "run_api" {
  service            = "run.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "eventarc_api" {
  service            = "eventarc.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloudfunctions_api" {
  service            = "cloudfunctions.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "artifactregistry_api" {
  service            = "artifactregistry.googleapis.com"
  disable_on_destroy = false
}

# === CAD Asset Bucket (public) ===
resource "google_storage_bucket" "cad_assets" {
  name                        = "theperfectkitebar-cad-assets"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_iam_binding" "public_access" {
  bucket  = google_storage_bucket.cad_assets.name
  role    = "roles/storage.objectViewer"
  members = ["allUsers"]
}

# === Function Code Bucket (private) ===
resource "google_storage_bucket" "fn_code" {
  name                        = "theperfectkitebar-fn-code"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_iam_binding" "fn_code_private" {
  bucket  = google_storage_bucket.fn_code.name
  role    = "roles/storage.objectViewer"
  members = [
    "projectOwner:${var.project_id}",
    "projectEditor:${var.project_id}",
  ]
}

# === Pub/Sub Topic for Budget Alerts ===
resource "google_pubsub_topic" "budget_alerts" {
  name = "cad-budget-alerts"
}

# === ZIP up each function (no *.bak) ===
data "archive_file" "disable_fn" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/functions-disable.zip"
  excludes    = ["**/*.bak"]
}

data "archive_file" "enable_fn" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/functions-enable.zip"
  excludes    = ["**/*.bak"]
}

# === Upload the ZIPs ===
resource "google_storage_bucket_object" "disable_zip" {
  name   = "functions-disable.zip"
  bucket = google_storage_bucket.fn_code.name
  source = data.archive_file.disable_fn.output_path
}

resource "google_storage_bucket_object" "enable_zip" {
  name   = "functions-enable.zip"
  bucket = google_storage_bucket.fn_code.name
  source = data.archive_file.enable_fn.output_path
}

# === Keep hardware/ in cad_assets ===
resource "google_storage_bucket_object" "shapr_placeholder" {
  name    = "hardware/.keep"
  bucket  = google_storage_bucket.cad_assets.name
  content = "placeholder"
}

# === disablePublicAccess (Gen 2, Pub/Sub) ===
resource "google_cloudfunctions2_function" "disable_access" {
  depends_on = [
    google_project_service.run_api,
    google_project_service.eventarc_api,
    google_project_service.cloudfunctions_api,
    google_project_service.artifactregistry_api
  ]
  name        = "disablePublicAccess"
  location    = var.region
  description = "Disables public access when budget exceeded"

  build_config {
    runtime     = "python312"
    entry_point = "disable_bucket_public_access"

    source {
      storage_source {
        bucket = google_storage_bucket.fn_code.name
        object = google_storage_bucket_object.disable_zip.name
      }
    }

    # force a new deploy whenever the ZIP changes
    environment_variables = {
      ZIP_HASH = data.archive_file.disable_fn.output_base64sha256
    }
  }

  service_config {
    available_memory   = "128Mi"
    timeout_seconds    = 60
    min_instance_count = 0
    max_instance_count = 3

    environment_variables = {
      BUCKET_NAME         = google_storage_bucket.cad_assets.name
      BUDGET_DISPLAY_NAME = var.budget_display_name
    }
  }

  event_trigger {
    event_type   = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic = google_pubsub_topic.budget_alerts.id
  }
}

# === enablePublicAccess (Gen 2, HTTP) ===
resource "google_cloudfunctions2_function" "enable_access" {
  depends_on = [
    google_project_service.run_api,
    google_project_service.eventarc_api,
    google_project_service.cloudfunctions_api,
    google_project_service.artifactregistry_api
  ]
  name        = "enablePublicAccess"
  location    = var.region
  description = "Re-enables public access monthly"

  build_config {
    runtime     = "python312"
    entry_point = "enable_bucket_public_access"

    source {
      storage_source {
        bucket = google_storage_bucket.fn_code.name
        object = google_storage_bucket_object.enable_zip.name
      }
    }

    environment_variables = {
      ZIP_HASH = data.archive_file.enable_fn.output_base64sha256
    }
  }

  service_config {
    available_memory   = "128Mi"
    timeout_seconds    = 60
    min_instance_count = 0
    max_instance_count = 3
    ingress_settings   = "ALLOW_ALL"

    environment_variables = {
      BUCKET_NAME = google_storage_bucket.cad_assets.name
    }
  }
}

# Allow public invocation of the HTTP-enable function (underlying Cloud Run service)
resource "google_cloud_run_v2_service_iam_member" "enable_invoker" {
  project  = var.project_id
  location = var.region
  name     = google_cloudfunctions2_function.enable_access.service_config[0].service
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# === Monthly re-enable job ===
resource "google_cloud_scheduler_job" "monthly_reenable" {
  name             = "reenable-public-access"
  description      = "Re-enable GCS public access each month"
  schedule         = "0 0 1 * *"
  time_zone        = "America/Toronto"
  attempt_deadline = "60s"

  http_target {
    http_method = "POST"
    uri         = google_cloudfunctions2_function.enable_access.service_config[0].uri
    oidc_token {
      service_account_email = google_cloudfunctions2_function.enable_access.service_config[0].service_account_email
    }
  }

  region  = var.region
  project = var.project_id
}

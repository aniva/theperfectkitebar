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

# 1) Public CAD-assets bucket
resource "google_storage_bucket" "cad_assets" {
  name                        = "theperfectkitebar-cad-assets"
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = true
}

resource "google_storage_bucket_iam_binding" "public_access" {
  bucket = google_storage_bucket.cad_assets.name
  role   = "roles/storage.objectViewer"
  members = ["allUsers"]
}

# 2) Private bucket for our function ZIPs
resource "google_storage_bucket" "fn_code" {
  name                        = "theperfectkitebar-fn-code"
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = true
}

resource "google_storage_bucket_iam_binding" "fn_code_private" {
  bucket = google_storage_bucket.fn_code.name
  role   = "roles/storage.objectViewer"
  members = [
    "projectOwner:${var.project_id}",
    "projectEditor:${var.project_id}",
  ]
}

# 3) Pub/Sub topic for budget alerts
resource "google_pubsub_topic" "budget_alerts" {
  name = "budget-alerts"
}

# 4) Build two ZIPs (disable vs enable), excluding .bak
data "archive_file" "disable_fn" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  excludes    = ["**/*.bak"]
  output_path = "${path.module}/functions-disable.zip"
}

data "archive_file" "enable_fn" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  excludes    = ["**/*.bak"]
  output_path = "${path.module}/functions-enable.zip"
}

# 5) Upload the ZIPs
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

# 6) Keep the empty placeholder so `hardware/` isn’t pruned
resource "google_storage_bucket_object" "shapr_placeholder" {
  name    = "hardware/.keep"
  bucket  = google_storage_bucket.cad_assets.name
  content = "placeholder"
}

# 7) disablePublicAccess — Gen-2, Pub/Sub trigger
resource "google_cloudfunctions2_function" "disable_access" {
  name     = "disablePublicAccess"
  location = var.region
  description = "Disables public access when budget exceeded"

  build_config {
    runtime     = "python310"
    entry_point = "disable_bucket_public_access"

    source {
      storage_source {
        bucket = google_storage_bucket.fn_code.name
        object = google_storage_bucket_object.disable_zip.name
      }
    }

    # force redeployment when code changes
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

# 8) enablePublicAccess — Gen-2, HTTP trigger
resource "google_cloudfunctions2_function" "enable_access" {
  name     = "enablePublicAccess"
  location = var.region
  description = "Re-enables public access monthly"

  build_config {
    runtime     = "python310"
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

  # THIS makes it an HTTP-triggered Gen-2 function:
  https_trigger {}
}

# 9) Allow “allUsers” to hit our HTTP-triggered function
resource "google_cloudfunctions2_function_iam_member" "enable_invoker" {
  project        = var.project_id
  location       = var.region
  cloud_function = google_cloudfunctions2_function.enable_access.name
  role           = "roles/run.invoker"
  member         = "allUsers"
}

# 10) Monthly job to call the HTTP-triggered enable function
resource "google_cloud_scheduler_job" "monthly_reenable" {
  name             = "reenable-public-access"
  description      = "Call enablePublicAccess monthly"
  schedule         = "0 0 1 * *"
  time_zone        = "America/Toronto"
  attempt_deadline = "60s"

  http_target {
    http_method = "POST"
    uri         = google_cloudfunctions2_function.enable_access.uri
    oidc_token {
      service_account_email = google_cloudfunctions2_function.enable_access.service_account_email
    }
  }

  region  = var.region
  project = var.project_id
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

data "google_project" "project" {
  project_id = var.project_id
}

# Artifact Registryのリポジトリを作成
resource "google_artifact_registry_repository" "test_repository" {
  location        = var.region
  repository_id   = "ai-agent-travel-llm-repository"
  format          = "DOCKER"
  description     = "Artifact Registry for Docker images"
  lifecycle {
    prevent_destroy = true  # リソースの破棄防止
    ignore_changes  = [description]
  }
}

# Firestore の作成
resource "google_firestore_database" "default" {
  name         = "ai-agent-travel-llm-firestore"
  project      = var.project_id
  location_id  = "nam5"
  type         = "FIRESTORE_NATIVE"  # FIRESTORE_NATIVE または DATASTORE_MODE
    
  lifecycle {
    prevent_destroy = true
  }
}

# サービスアカウントの作成
resource "google_service_account" "cloud_run_sa" {
  account_id   = "travel-agent-cloud-run-sa"
  display_name = "Service Account for Cloud Run"
  lifecycle {
    prevent_destroy = true
  }
}

# Vertex AI アクセス権限の付与
resource "google_project_iam_member" "vertex_ai_access" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.cloud_run_sa.email}"
  depends_on = [google_service_account.cloud_run_sa]
}

# Firestore アクセス権限の付与
resource "google_project_iam_member" "firestore_access" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.cloud_run_sa.email}"
  depends_on = [google_service_account.cloud_run_sa]
}

# Secret Managerの作成
resource "google_secret_manager_secret" "secret" {
  secret_id = "travel-llm-secret"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "secret-version-data" {
  secret = google_secret_manager_secret.secret.name
  secret_data = "secret-data"
}

# Secret Managerのアクセス権限の付与
resource "google_secret_manager_secret_iam_member" "secret-access" {
  secret_id = google_secret_manager_secret.secret.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_run_sa.email}"
  depends_on = [google_secret_manager_secret.secret]
}


# Cloud Run サービスの定義
resource "google_cloud_run_v2_service" "llm_service" {
  name     = "llm-run-service"
  location = var.region
  deletion_protection = false
  ingress = "INGRESS_TRAFFIC_ALL"

  template {
      containers {
        image = "asia-northeast1-docker.pkg.dev/${var.project_id}/ai-agent-travel-llm-repository/llm-run-service:latest"
        env {
            name = "SECRET_ENV_VAR"
            value_source {
            secret_key_ref {
                secret = google_secret_manager_secret.secret.secret_id
                version = "1"
                }
            }
        }
        ports {
            container_port = var.port  # カスタムポート番号
        }
      }
      service_account = google_service_account.cloud_run_sa.email
  }
  depends_on = [google_secret_manager_secret_version.secret-version-data]
}

# TODO: GEMINI アクセス用の権限付与する

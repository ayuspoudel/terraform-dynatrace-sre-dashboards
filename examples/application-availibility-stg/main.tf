terraform {
  required_providers {
    dynatrace = {
      source  = "dynatrace-oss/dynatrace"
      version = "~> 1.19.0"
    }
  }
}

provider "dynatrace" {
  dt_env_url   = var.dynatrace_api_url # e.g. https://abc123.live.dynatrace.com/api
  dt_api_token = var.dynatrace_api_token
}

# locals {
#   error_rate_dql = file("${path.module}/dql/error_rate_by_service.dql")
# }

resource "dynatrace_dashboard" "errors_dash" {
  dashboard_metadata {
    name   = "Ayush V2"
    shared = true
    owner  = "ayushpoudel2003@gmail.com"
    tags   = ["Kubernetes"]
    dynamic_filters {
      filters = ["KUBERNETES_CLUSTER"]
    }
  }
  tile {
    name       = "Service Errors"
    tile_type  = "DATA_EXPLORER"
    configured = true
    bounds {
      top    = 0
      left   = 0
      width  = 76
      height = 76 # ✅ multiple of 38 (e.g., 38, 76, 114, etc.)
    }
    custom_name = "Error Rate by Service"
  }

}

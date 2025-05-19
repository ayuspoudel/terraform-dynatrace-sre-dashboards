terraform {
  required_providers {
    dynatrace = {
      source  = "dynatrace-oss/dynatrace"
      version = "~> 1.19.0"
    }
  }
}

provider "dynatrace" {
  dt_env_url   = var.dynatrace_api_url   # e.g. https://abc123.live.dynatrace.com/api
  dt_api_token = var.dynatrace_api_token
}

# (1) 前提値: project=skillax, env=prod なので name_prefix は "skillax-prod"
# (2) for_each は local.services の3キー(api, web, worker)分 → 3個できる
# (3) 名前は "<prefix>-<キー>"、タグは common_tags に Name を merge したもの
variable "project" {
  default = "skillax"
}

variable "env" {
  default = "prod"
}

locals {
  name_prefix = "${var.project}-${var.env}"
  common_tags = {
    Project   = var.project
    Env       = var.env
    ManagedBy = "terraform"
  }
  services = {
    api    = { port = 8080 }
    web    = { port = 80 }
    worker = { port = 0 }
  }
}

output "api_tags" {
  value = jsonencode(merge(local.common_tags, { Name = "${local.name_prefix}-api" }))
}

output "service_count" {
  value = length(local.services)
}

output "service_names" {
  value = join(", ", [for k in keys(local.services) : "${local.name_prefix}-${k}"])
}

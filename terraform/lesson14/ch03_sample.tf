# 読解3ステップ: (1) 前提値の確定 (2) for_each の数 (3) 組み立て式に代入
variable "project" {
  default = "app"
}

variable "env" {
  default = "dev"
}

locals {
  name_prefix = "${var.project}-${var.env}"
  services = {
    api = { port = 8080 }
    web = { port = 80 }
  }
}

# resource "aws_ecs_service" "this" { for_each = local.services ... } を想定
output "service_count" {
  value = length(local.services)
}

output "service_names" {
  value = join(", ", [for k in keys(local.services) : "${local.name_prefix}-${k}"])
}

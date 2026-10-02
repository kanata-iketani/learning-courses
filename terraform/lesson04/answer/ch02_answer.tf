# "${式}" が文字列補間。実務の「プロジェクト名-環境名」の組み立てそのものです。
# 数値の計算は locals の右辺に演算子でそのまま書けます。
variable "app" {
  type    = string
  default = "billing"
}

variable "env" {
  type    = string
  default = "prod"
}

locals {
  name           = "${var.app}-${var.env}"
  total_capacity = 4 * 3
}

output "resource_name" {
  value = local.name
}

output "total_capacity" {
  value = local.total_capacity
}

# lesson04 ch03: 条件式
# 条件 ? 真の値 : 偽の値 で切り替えます。

variable "env" {
  type    = string
  default = "dev"
}

locals {
  # env が prod なら large、それ以外は small
  instance_type = var.env == "prod" ? "large" : "small"

  # 比較演算子の結果は bool
  is_production = var.env == "prod"
}

output "instance_type" {
  value = local.instance_type # default が dev なので small
}

output "is_production" {
  value = local.is_production
}

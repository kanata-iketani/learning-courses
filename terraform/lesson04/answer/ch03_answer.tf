# 条件式は 条件 ? 真の値 : 偽の値。env による切り替えの定番パターンです。
# 比較 var.env == "prod" は bool になるので、そのまま output にも出せます。
variable "env" {
  type    = string
  default = "prod"
}

locals {
  instance_type = var.env == "prod" ? "large" : "small"
}

output "instance_type" {
  value = local.instance_type
}

output "is_production" {
  value = var.env == "prod"
}

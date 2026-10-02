# 「env 名で設定値を出し分ける」核のパターンです。
# terraform.workspace の代わりに variable で環境名を受け取ります。

variable "env" {
  type    = string
  default = "prod"
}

locals {
  is_prod  = var.env == "prod"
  min_size = local.is_prod ? 4 : 1
}

output "env" {
  value = var.env
}

output "min_size" {
  value = local.min_size
}

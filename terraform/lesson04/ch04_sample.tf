# lesson04 ch04: locals 集約スタイル
# 組み立てを locals に寄せると、使う側は local.xxx だけになります。

variable "project" {
  type    = string
  default = "myapp"
}

variable "env" {
  type    = string
  default = "dev"
}

locals {
  # 共通の接頭辞をここで一度だけ組み立てます
  name_prefix = "${var.project}-${var.env}"

  # locals は locals を参照できます(local. で参照)
  log_bucket = "${local.name_prefix}-logs"
}

output "name_prefix" {
  value = local.name_prefix
}

output "log_bucket" {
  value = local.log_bucket
}

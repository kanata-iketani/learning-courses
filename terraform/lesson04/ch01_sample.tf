# lesson04 ch01: locals と local.
# variable は「外からの入力」、locals は「中で付けた名前」です。

variable "team" {
  type    = string
  default = "platform"
}

locals {
  # 定義は locals(複数形)ブロックにまとめて書きます
  retention_days = 14
  managed_by     = "terraform"
}

output "owner_team" {
  value = var.team # 外からの入力は var.
}

output "managed_by" {
  value = local.managed_by # 中で付けた名前は local.
}

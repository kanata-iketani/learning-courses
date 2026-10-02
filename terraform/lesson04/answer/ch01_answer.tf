# 外から差し替えたい値は variable、中で組み立てる値は locals に置きます。
# 定義は locals(複数形)、参照は local.名前(単数形)です。
variable "team" {
  type    = string
  default = "sre"
}

locals {
  retention_days = 30
}

output "owner_team" {
  value = var.team
}

output "retention" {
  value = local.retention_days
}

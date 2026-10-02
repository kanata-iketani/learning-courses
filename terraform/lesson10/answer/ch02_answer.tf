# 引数 team / system がモジュール側の variable への入力になります。
module "labels" {
  source = "./modules/labels"
  team   = "platform"
  system = "billing"
}

# モジュールの値は module.labels.label のように output 経由でだけ受け取れます
output "label" {
  value = module.labels.label
}

# === file: modules/labels/main.tf ===
variable "team" {
  type = string
}

variable "system" {
  type = string
}

locals {
  label = "team:${var.team}/system:${var.system}"
}

# locals のままでは外から見えないため、output で公開します
output "label" {
  value = local.label
}

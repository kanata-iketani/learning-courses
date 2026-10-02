# 入力(variable)→ 加工 → 出力(output)というモジュールの基本形です。

module "tags" {
  source = "./modules/tagger"
  env    = "stg"
  owner  = "sre"
}

output "tag_line" {
  value = module.tags.tag_line # output で公開された値だけが見える
}

# === file: modules/tagger/main.tf ===
variable "env" {
  type = string
}

variable "owner" {
  type = string
}

# locals はモジュール内部だけの値。外に返すには output が必要です
locals {
  tag_line = "env=${var.env} owner=${var.owner}"
}

output "tag_line" {
  value = local.tag_line
}

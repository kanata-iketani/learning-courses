# 流儀が違っても最終的な値は同じです。フラット派は grep で追いやすく、
# モジュール派は再利用しやすい、というトレードオフを体感するのが狙いです。
variable "project" {
  default = "skillax"
}

variable "env" {
  default = "prod"
}

# 流儀1: フラットにその場で組み立てる
locals {
  flat_name = "${var.project}-${var.env}-logs"
}

# 流儀2: 組み立てロジックはモジュール側にある
module "naming" {
  source  = "./modules/naming"
  project = var.project
  env     = var.env
}

output "flat_name" {
  value = local.flat_name
}

output "module_name" {
  value = module.naming.bucket_name
}

output "same_result" {
  value = local.flat_name == module.naming.bucket_name ? "yes" : "no"
}

# === file: modules/naming/main.tf ===
# モジュール側: 入力(variable)を受けて出力(output)で名前を返します
variable "project" {
  default = ""
}

variable "env" {
  default = ""
}

output "bucket_name" {
  value = "${var.project}-${var.env}-logs"
}

# 同じ名前を「フラット派」と「モジュール派」の両方で組み立てます。
variable "project" {
  default = "app"
}

variable "env" {
  default = "dev"
}

# 流儀1: フラット派はその場で組み立てる
locals {
  flat_name = "${var.project}-${var.env}-logs"
}

# 流儀2: モジュール派は組み立てをモジュールに任せる
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

# === file: modules/naming/main.tf ===
# モジュール側: variable(入力) → 組み立て → output(出力)の順に読みます
variable "project" {
  default = ""
}

variable "env" {
  default = ""
}

output "bucket_name" {
  value = "${var.project}-${var.env}-logs"
}

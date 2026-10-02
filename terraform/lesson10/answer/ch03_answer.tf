module "naming" {
  source = "./modules/naming"
  env    = "prod"
  app    = "skillax"
}

# terraform output はアルファベット順に表示されます(bucket_name が先)
output "resource_name" {
  value = module.naming.resource_name
}

output "bucket_name" {
  value = module.naming.bucket_name
}

# === file: modules/naming/main.tf ===
variable "env" {
  type = string
}

variable "app" {
  type = string
}

# 命名規約をこの 1 ファイルに集約。規約変更時はここだけ直せばよい
output "resource_name" {
  value = "${var.app}-${var.env}"
}

output "bucket_name" {
  value = "${var.app}-${var.env}-logs"
}

# env と app から名前を組み立てる naming モジュールの最小例です。

module "naming" {
  source = "./modules/naming"
  env    = "stg"
  app    = "api"
}

output "prefix" {
  value = module.naming.prefix
}

# === file: modules/naming/main.tf ===
variable "env" {
  type = string
}

variable "app" {
  type = string
}

# 命名規約「app名-環境名」をこのモジュールに集約する
output "prefix" {
  value = "${var.app}-${var.env}"
}

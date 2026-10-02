# モジュール本体は 1 つだけ。渡す env が違うだけで結果が変わります。
# 実務ではこの 2 ブロックが environments/prod と environments/stg に分かれて置かれます。
module "prod" {
  source = "./modules/service"
  env    = "prod"
}

module "stg" {
  source = "./modules/service"
  env    = "stg"
}

output "prod_type" {
  value = module.prod.instance_type
}

output "stg_type" {
  value = module.stg.instance_type
}

# === file: modules/service/main.tf ===
variable "env" {
  type = string
}

output "name" {
  value = "app-${var.env}"
}

output "instance_type" {
  value = var.env == "prod" ? "m5.large" : "t3.small"
}

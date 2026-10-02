# 同じモジュールに違う env を渡すと出力が変わることを 1 ファイルで体験します。
# 実際は prod/ と stg/ の別ディレクトリに置かれる 2 つの呼び出しです。

module "prod" {
  source = "./modules/service"
  env    = "prod"
}

module "stg" {
  source = "./modules/service"
  env    = "stg"
}

output "prod_name" {
  value = module.prod.name
}

output "stg_name" {
  value = module.stg.name
}

# === file: modules/service/main.tf ===
variable "env" {
  type = string
}

output "name" {
  value = "app-${var.env}"
}

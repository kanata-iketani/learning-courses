variable "buckets" {
  default = ["logs-prod", "logs-dev", "assets-prod", "tmp-dev"]
}

# if は「: 式」の後ろに置きます。endswith でサフィックス判定するのが実務の定番です。
# 元リストの順序は保たれるので、logs-prod → assets-prod の順になります。
locals {
  prod = [for b in var.buckets : b if endswith(b, "-prod")]
}

output "prod_buckets" {
  value = join(",", local.prod)
}

output "prod_count" {
  value = length(local.prod)
}

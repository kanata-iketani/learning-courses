# lesson04 ch02: 文字列補間と演算子
# "${}" で文字列の中に式を埋め込めます。

variable "app" {
  type    = string
  default = "web"
}

variable "env" {
  type    = string
  default = "dev"
}

locals {
  # 実務で最頻出の「名前の組み立て」パターン
  name = "${var.app}-${var.env}"

  # 算術演算子も使えます
  total_gb = 20 * 2
}

output "resource_name" {
  value = local.name
}

output "total_gb" {
  value = local.total_gb
}

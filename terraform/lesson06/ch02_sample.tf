# lesson06 ch02: マップを作る for 式
variable "sizes" {
  default = {
    api = "t3.medium"
    web = "t3.small"
  }
}

variable "names" {
  default = ["sato", "suzuki"]
}

locals {
  # k にキー、v に値。=> の右で新しい値を組み立てます
  labels = { for k, v in var.sizes : k => "${k} runs on ${v}" }

  # リストからマップを作ることもできます
  name_len = { for n in var.names : n => length(n) }
}

output "web_label" {
  value = local.labels["web"]
}

output "sato_len" {
  value = local.name_len["sato"]
}

output "label_keys" {
  value = join(",", keys(local.labels))
}

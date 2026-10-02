variable "sizes" {
  default = {
    api = "t3.medium"
    web = "t3.small"
  }
}

# {for k, v in マップ : k => 式} は「キーを保ったまま値だけ作り替える」定番形です。
# keys / values はアルファベット順なので、label_values も api → web の順になります。
locals {
  labels = { for k, v in var.sizes : k => "${k}:${v}" }
}

output "label_keys" {
  value = join(",", keys(local.labels))
}

output "label_values" {
  value = join(" ", values(local.labels))
}

output "web" {
  value = local.labels["web"]
}

# count のアドレスはリストの添字、for_each のアドレスは名前(キー)です。
# moved ブロックには from = 旧アドレス / to = 新アドレスとしてこの対応が
# そのまま書かれるので、この変換が読めれば移行の痕跡を追えます。
variable "names" {
  default = ["blue", "green"]
}

output "new_addresses" {
  value = join(", ", [for n in var.names : "terraform_data.web[\"${n}\"]"])
}

output "old_addresses" {
  value = join(", ", [for i, n in var.names : "terraform_data.web[${i}]"])
}

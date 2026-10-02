# split(".", "5.67.3") は ["5", "67", "3"] という文字列リストになります。
# ~> 5.67 という制約なら major(5) は固定で minor 以下の更新だけ許される、
# という読み方がこの分解と対応しています。
variable "provider_version" {
  default = "5.67.3"
}

locals {
  parts = split(".", var.provider_version)
}

output "major" {
  value = tonumber(local.parts[0])
}

output "minor" {
  value = tonumber(local.parts[1])
}

output "patch" {
  value = tonumber(local.parts[2])
}

# lesson06 ch01: リストの for 式
variable "names" {
  default = ["ayame", "botan", "kaede"]
}

locals {
  # 各要素に upper をかけた新しいリストを作ります
  upper_names = [for n in var.names : upper(n)]

  # i には 0 始まりの index が入ります
  hosts = [for i, n in var.names : format("%02d-%s", i + 1, n)]
}

output "upper_joined" {
  value = join(",", local.upper_names)
}

output "hosts" {
  value = join(",", local.hosts)
}

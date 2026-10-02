variable "vpcs" {
  type = list(object({
    name    = string
    subnets = list(string)
  }))
  default = [
    { name = "main", subnets = ["10.0.1.0/24", "10.0.2.0/24"] },
    { name = "edge", subnets = ["10.9.1.0/24"] },
  ]
}

# var.vpcs[*].subnets は list(list(string)) になるため flatten で1段に平坦化します。
# 「全 VPC のサブネット ID を1本にまとめる」実務パターンそのままの形です。
locals {
  all_subnets = flatten(var.vpcs[*].subnets)
}

output "subnet_count" {
  value = length(local.all_subnets)
}

output "subnets" {
  value = join(",", local.all_subnets)
}

output "vpc_names" {
  value = join(",", var.vpcs[*].name)
}

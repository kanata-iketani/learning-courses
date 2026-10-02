# lesson05 ch02: コレクション関数
variable "base_ports" {
  default = ["80", "443"]
}

variable "extra_ports" {
  default = ["8080"]
}

variable "limits" {
  default = {
    cpu    = "2"
    memory = "4Gi"
  }
}

locals {
  # concat で複数のリストを1本に連結します
  ports = concat(var.base_ports, var.extra_ports)
}

output "port_count" {
  value = length(local.ports)
}

output "ports" {
  value = join(",", local.ports)
}

output "has_https" {
  value = contains(local.ports, "443")
}

# keys / values はキーのアルファベット順で返ります
output "limit_keys" {
  value = join(",", keys(var.limits))
}

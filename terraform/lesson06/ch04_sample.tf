# lesson06 ch04: splat と flatten
variable "servers" {
  type = list(object({
    name = string
    ips  = list(string)
  }))
  default = [
    { name = "web", ips = ["10.0.0.1", "10.0.0.2"] },
    { name = "db", ips = ["10.0.1.1"] },
  ]
}

# splat: [*] は「全要素の name をまとめて取り出す」
output "names" {
  value = join(",", var.servers[*].name)
}

# ips を splat すると「リストのリスト」になるので flatten で1段にします
output "all_ips" {
  value = join(",", flatten(var.servers[*].ips))
}

output "ip_count" {
  value = length(flatten(var.servers[*].ips))
}

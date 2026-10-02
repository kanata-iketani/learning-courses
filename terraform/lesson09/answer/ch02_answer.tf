variable "ingress_rules" {
  type = list(object({ port = number, cidr = string }))
  default = [
    { port = 22, cidr = "10.0.0.0/8" },
    { port = 443, cidr = "0.0.0.0/0" },
  ]
}

# iterator = rule のときの rule.value.port は、for 式では r.port に対応します。
# dynamic の content 1 回分 = for 式の 1 要素、という対応で読み替えます。
locals {
  lines = [for r in var.ingress_rules : "${r.port} from ${r.cidr}"]
}

output "ingress" {
  value = join(", ", local.lines)
}

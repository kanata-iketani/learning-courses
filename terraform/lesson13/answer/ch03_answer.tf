# dynamic "ingress" は for_each の要素ごとに ingress ブロックを1つ生成します。
# つまりルール数は元リストの長さと同じで、内容は for 式でそのまま言語化できます。
variable "ingress_ports" {
  default = [80, 443, 8080]
}

locals {
  rules = [for p in var.ingress_ports : "allow tcp/${p} from 10.0.0.0/8"]
}

output "rule_count" {
  value = length(local.rules)
}

output "rules" {
  value = join(", ", local.rules)
}

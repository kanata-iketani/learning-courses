variable "allowed_ports" {
  type    = list(number)
  default = [22, 80, 443]
}

# dynamic "ingress" { for_each = var.allowed_ports ... } と同じ繰り返しです。
# dynamic が port の数だけ content を生成するのと同様に、
# for 式は要素の数だけルール文字列を生成します。
locals {
  rules = [for p in var.allowed_ports : format("%d-%d/tcp", p, p)]
}

output "rules" {
  value = join(", ", local.rules)
}

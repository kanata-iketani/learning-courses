# ベタ書きされていた ingress を「ポートのリスト」に還元して読む練習です。
variable "ingress_ports" {
  default = [80, 443]
}

variable "internal_cidr" {
  default = "10.0.0.0/8"
}

locals {
  # dynamic "ingress" が生成するルールを for 式で言語化します
  rules = [for p in var.ingress_ports : "tcp/${p} from ${var.internal_cidr}"]
}

output "rule_count" {
  value = length(local.rules)
}

output "rules" {
  value = join(", ", local.rules)
}

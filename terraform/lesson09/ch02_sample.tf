# text の dynamic + iterator が生成するルールを for 式で再現します。
# rule.value.port / rule.value.cidr の読み方は、for 式の r.port / r.cidr と同じです。

locals {
  ingress_rules = [
    { port = 80, cidr = "10.0.0.0/16" },
    { port = 443, cidr = "0.0.0.0/0" },
  ]

  # 1 要素が content 1 回分に対応する
  lines = [for r in local.ingress_rules : "${r.port} from ${r.cidr}"]
}

output "ingress" {
  value = join(", ", local.lines)
}

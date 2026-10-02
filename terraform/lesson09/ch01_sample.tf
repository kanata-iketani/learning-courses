# text の dynamic ブロックが生成する ingress ルールを、
# lesson06 で学んだ for 式で「見える化」してみます。
# dynamic は書けなくても、この繰り返しロジックが読めれば十分です。

locals {
  ports = [80, 443]

  # 各ポートから "80-80/tcp" 形式のルール文字列を作る
  rules = [for p in local.ports : format("%d-%d/tcp", p, p)]
}

output "rule_count" {
  value = length(local.rules)
}

output "rules" {
  value = join(", ", local.rules)
}

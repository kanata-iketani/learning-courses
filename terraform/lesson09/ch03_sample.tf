# 「件数が可変かどうか」で dynamic を使うべきかを判定するロジックの例です。
# 実務の判断基準を条件式にしてみます。

locals {
  rules = ["http", "https", "ssh", "monitoring"]

  # 件数が多い(またはリストが variable 由来)なら dynamic が候補になる
  decision = length(local.rules) >= 3 ? "dynamic" : "static"
}

output "decision" {
  value = local.decision
}

output "rule_count" {
  value = length(local.rules)
}

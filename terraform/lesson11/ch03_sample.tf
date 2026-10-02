# チェックリストを for 式で番号付きに整形する例です。
# lesson06 で学んだ「インデックス付き for 式」を使います。

locals {
  steps = ["backend", "provider", "variables", "main"]

  # for 式は「for インデックス, 値 in リスト」の形でも書けます(インデックスは 0 始まり)
  numbered = [for i, s in local.steps : "${i + 1}. ${s}"]
}

output "first_step" {
  value = local.numbered[0]
}

output "step_count" {
  value = length(local.steps)
}

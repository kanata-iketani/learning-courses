# lesson01 ch03: apply すると state に記録されます
# 「▶ 実行」は init → apply → output の一括実行です。

resource "terraform_data" "tracked" {
  input = "stateで管理"
}

# apply が終わると、このリソースは state に記録されます。
# もう一度 apply しても差分がなければ何も起きません(冪等性)。

output "tracked" {
  value = terraform_data.tracked.output
}

output "cycle" {
  value = "init-plan-apply"
}

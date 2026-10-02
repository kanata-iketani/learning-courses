# apply されたリソースは state に記録され、output は apply 後の値を表示します。
# 同じコードを何度 apply しても結果が変わらないのが宣言的スタイルの利点です。
resource "terraform_data" "tracked" {
  input = "stateで管理"
}

output "cycle" {
  value = "plan-apply"
}

output "tracked" {
  value = terraform_data.tracked.output
}

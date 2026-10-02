variable "users" {
  default = ["sato", "suzuki", "takahashi"]
}

# for 式は「元のリストは変えず、変換後の新しいリストを作る」のがポイントです。
# "${u}@..." のような文字列テンプレートとの組み合わせが実務の定番です。
locals {
  emails = [for u in var.users : "${u}@example.com"]
}

output "email_count" {
  value = length(local.emails)
}

# リストの output は複数行の tolist([...]) 形式で表示されます
output "emails" {
  value = tolist(local.emails)
}

output "joined" {
  value = join(",", local.emails)
}

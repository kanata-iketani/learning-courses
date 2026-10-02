# lesson08 ch01: set で for_each
variable "users" {
  default = ["sato", "suzuki"]
}

resource "terraform_data" "user" {
  # リストは toset で set にしてから渡します
  for_each = toset(var.users)
  # each.value が今の要素("sato" や "suzuki")です
  input = format("user-%s", each.value)
}

# for_each のリソースは「要素をキーとするマップ」になります
output "sato" {
  value = terraform_data.user["sato"].output
}

output "user_keys" {
  value = join(",", keys(terraform_data.user))
}

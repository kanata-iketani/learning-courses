# state はコードと実リソースの対応表。apply のたびに更新されます。
# この2つのリソースは state に「型.名前」のアドレスで記録されます。
resource "terraform_data" "app" {
  input = "app-server"
}

resource "terraform_data" "db" {
  input = "db-server"
}

# terraform state list で見えるアドレスのイメージ
output "state_addresses" {
  value = join(", ", ["terraform_data.app", "terraform_data.db"])
}

# state が管理しているリソース数(state を手で消すとこの対応が失われます)
output "managed_count" {
  value = 2
}

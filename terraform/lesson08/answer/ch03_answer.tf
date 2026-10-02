variable "topics" {
  default = ["audit", "mail", "sync"]
}

resource "terraform_data" "topic" {
  for_each = toset(var.topics)
  input    = format("topic-%s", each.value)
}

# for_each のリソースはマップなので、全要素は values() でリスト化 → [*] で属性取得します。
# values() はキーのアルファベット順なので audit → mail → sync の順に並びます。
output "all_topics" {
  value = join(",", values(terraform_data.topic)[*].output)
}

output "mail" {
  value = terraform_data.topic["mail"].output
}

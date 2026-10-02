# lesson08 ch03: for_each リソースの参照
variable "queues" {
  default = ["mail", "sync"]
}

resource "terraform_data" "queue" {
  for_each = toset(var.queues)
  input    = format("queue-%s", each.value)
}

# マップなので [0] ではなく ["キー"] で個別参照します
output "mail" {
  value = terraform_data.queue["mail"].output
}

# 全要素は values() でリスト化してから splat で属性を取り出します
output "all" {
  value = join(",", values(terraform_data.queue)[*].output)
}

output "queue_count" {
  value = length(terraform_data.queue)
}

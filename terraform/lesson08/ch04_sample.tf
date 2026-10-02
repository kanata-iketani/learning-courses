# lesson08 ch04: count 版と for_each 版の比較
variable "envs" {
  default = ["dev", "prod", "stg"]
}

# count 版: リストの位置で管理される(増減に弱い)
resource "terraform_data" "by_count" {
  count = length(var.envs)
  input = var.envs[count.index]
}

# for_each 版: 要素の値がキーになる(増減に強い)
resource "terraform_data" "by_each" {
  for_each = toset(var.envs)
  input    = each.value
}

# 参照の形も変わります: count はリスト、for_each はマップ
output "count_style" {
  value = join(",", terraform_data.by_count[*].output)
}

output "each_keys" {
  value = join(",", keys(terraform_data.by_each))
}

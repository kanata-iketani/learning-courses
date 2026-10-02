variable "before" {
  default = ["app-a", "app-b", "app-c"]
}

variable "after" {
  default = ["app-a", "app-c"]
}

# before では app-c が index 2 ですが、真ん中を消した after では index 1 に繰り上がります。
# 実際の運用では「同じ app-c なのに位置が変わった」ことで作り直しが計画されます。
resource "terraform_data" "before" {
  count = length(var.before)
  input = format("%d:%s", count.index, var.before[count.index])
}

resource "terraform_data" "after" {
  count = length(var.after)
  input = format("%d:%s", count.index, var.after[count.index])
}

output "after_pairs" {
  value = join(" ", terraform_data.after[*].output)
}

output "before_pairs" {
  value = join(" ", terraform_data.before[*].output)
}

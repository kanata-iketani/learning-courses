# lesson05 ch01: 文字列関数
variable "project" {
  default = "myapp"
}

variable "env" {
  default = "Prod"
}

locals {
  # format は printf 風の文字列組み立て。lower で表記ゆれを正規化するのが定番です
  name = format("%s-%s", var.project, lower(var.env))

  # split は文字列をリストに分解します(join の逆)
  parts = split("-", local.name)
}

output "name" {
  value = local.name
}

output "first_part" {
  value = local.parts[0]
}

# replace で区切り文字を差し替え、upper で大文字化
output "shout" {
  value = upper(replace(local.name, "-", "_"))
}

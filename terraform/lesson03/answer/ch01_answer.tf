# variable は外部入力の宣言。default を付けると入力なしでも apply が通るので、
# この講座の演習では必ず default を付けます。参照は var.名前 です。
variable "project" {
  type    = string
  default = "skillax"
}

output "project_name" {
  value = var.project
}

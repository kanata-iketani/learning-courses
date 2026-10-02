variable "envs" {
  default = ["dev", "prod", "stg"]
}

# count.index による位置参照を each.value に置き換えるだけで同じものが作れます。
# for_each 版はキーが "dev"/"prod"/"stg" になるため、途中の要素を消しても
# 他のリソースが作り直しにならない、というのが現場で好まれる理由です。
resource "terraform_data" "env" {
  for_each = toset(var.envs)
  input    = format("env-%s", each.value)
}

output "env_keys" {
  value = join(",", keys(terraform_data.env))
}

output "prod" {
  value = terraform_data.env["prod"].output
}

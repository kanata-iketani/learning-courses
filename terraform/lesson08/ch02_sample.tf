# lesson08 ch02: map で for_each
variable "instances" {
  default = {
    api = "t3.medium"
    web = "t3.small"
  }
}

resource "terraform_data" "instance" {
  # マップはそのまま for_each に渡せます
  for_each = var.instances
  # each.key がキー(api/web)、each.value が値(タイプ)です
  input = format("%s runs on %s", each.key, each.value)
}

output "web" {
  value = terraform_data.instance["web"].output
}

output "instance_keys" {
  value = join(",", keys(terraform_data.instance))
}

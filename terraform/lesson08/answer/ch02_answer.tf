variable "instances" {
  default = {
    api = "t3.medium"
    web = "t3.small"
  }
}

# マップの for_each では each.key と each.value の両方が使えるのが set との違いです。
# 「名前 → 設定値」のマップを variable に持たせて回すのが実務の最頻出形です。
resource "terraform_data" "instance" {
  for_each = var.instances
  input    = format("%s=%s", each.key, each.value)
}

output "api" {
  value = terraform_data.instance["api"].output
}

output "instance_keys" {
  value = join(",", keys(terraform_data.instance))
}

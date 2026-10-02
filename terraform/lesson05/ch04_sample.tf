# lesson05 ch04: try / coalesce / jsonencode
variable "nickname" {
  default = "" # 「未設定」を空文字で表しています
}

variable "cfg" {
  type = map(string)
  default = {
    name = "app"
  }
}

locals {
  # coalesce は null と "" を飛ばして最初に値があるものを返します
  display = coalesce(var.nickname, "anonymous")

  # cfg に port キーは無いので try が既定値 "8080" に倒します
  port = try(var.cfg["port"], "8080")
}

output "display" {
  value = local.display
}

output "port" {
  value = local.port
}

# jsonencode は HCL の値を JSON 文字列にします(キーはアルファベット順)
output "as_json" {
  value = jsonencode({
    name = var.cfg["name"]
    port = local.port
  })
}

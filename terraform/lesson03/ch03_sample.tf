# lesson03 ch03: object 型
# 関連する設定をひとつの variable に束ねます。

variable "server" {
  type = object({
    name  = string
    port  = number
    https = bool
  })
  default = {
    name  = "api-server"
    port  = 8080
    https = true
  }
}

output "server_name" {
  # 属性はドットで参照します
  value = var.server.name
}

output "server_port" {
  value = var.server.port
}

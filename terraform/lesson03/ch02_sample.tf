# lesson03 ch02: 型いろいろ
# list は [0] で、map は ["キー"] で要素を参照します。

variable "ports" {
  type    = list(number)
  default = [80, 443, 8080]
}

variable "tags" {
  type    = map(string)
  default = { env = "prod", team = "sre" }
}

variable "debug" {
  type    = bool
  default = true
}

output "first_port" {
  value = var.ports[0] # 0 始まり
}

output "team_tag" {
  value = var.tags["team"]
}

output "debug_mode" {
  value = var.debug
}

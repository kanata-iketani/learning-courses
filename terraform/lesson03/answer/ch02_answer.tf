# list は var.ports[0](0 始まり)、map は var.tags["env"] で要素参照します。
# 出力は number と bool がクォートなし、string だけダブルクォート付きになります。
variable "ports" {
  type    = list(number)
  default = [80, 443]
}

variable "tags" {
  type    = map(string)
  default = { env = "dev" }
}

variable "debug" {
  type    = bool
  default = false
}

output "debug_mode" {
  value = var.debug
}

output "env_tag" {
  value = var.tags["env"]
}

output "first_port" {
  value = var.ports[0]
}

variable "enable_logging" {
  default = true
}

variable "enable_monitoring" {
  default = false
}

# 「? 1 : 0」はフラグでリソースを作る/作らないを切り替える実務の定番イディオムです。
# count = 0 のときは [0] 参照がエラーになるため、try で "off" に倒して参照します。
resource "terraform_data" "logging" {
  count = var.enable_logging ? 1 : 0
  input = "logging-on"
}

resource "terraform_data" "monitoring" {
  count = var.enable_monitoring ? 1 : 0
  input = "monitoring-on"
}

output "logging" {
  value = try(terraform_data.logging[0].output, "off")
}

output "logging_count" {
  value = length(terraform_data.logging)
}

output "monitoring" {
  value = try(terraform_data.monitoring[0].output, "off")
}

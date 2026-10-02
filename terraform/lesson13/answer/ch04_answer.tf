# cpu は var.container_cpu が 0(未指定)なので条件式の右側 256 に確定します。
# memory は var.container_memory の default 1024 がそのまま使われます。
# 「var. を見たら default と上書き経路を確認する」のが読解の基本です。
variable "container_cpu" {
  default = 0
}

variable "container_memory" {
  default = 1024
}

locals {
  cpu    = var.container_cpu > 0 ? var.container_cpu : 256
  memory = var.container_memory
}

output "cpu" {
  value = local.cpu
}

output "cpu_source" {
  value = var.container_cpu > 0 ? "variable" : "hardcoded-default"
}

output "memory" {
  value = local.memory
}

output "memory_source" {
  value = "variable-default"
}

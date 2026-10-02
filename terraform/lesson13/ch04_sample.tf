# 「0 や空なら既定値」という折衷パターン。値の出どころを条件式で明示します。
variable "container_cpu" {
  default = 0 # 0 は「未指定」の意味で使う流儀
}

locals {
  default_cpu   = 256
  effective_cpu = var.container_cpu > 0 ? var.container_cpu : local.default_cpu
  cpu_source    = var.container_cpu > 0 ? "variable" : "hardcoded-default"
}

output "cpu_source" {
  value = local.cpu_source
}

output "effective_cpu" {
  value = local.effective_cpu
}

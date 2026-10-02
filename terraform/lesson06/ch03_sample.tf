# lesson06 ch03: if でフィルタする for 式
variable "hosts" {
  default = ["web-prod", "web-dev", "db-prod", "cache-dev"]
}

locals {
  # if 条件を満たす要素だけが残ります
  prod_hosts = [for h in var.hosts : h if endswith(h, "-prod")]

  # フィルタと変換は同時にできます(dev だけを大文字に)
  dev_upper = [for h in var.hosts : upper(h) if endswith(h, "-dev")]
}

output "prod_hosts" {
  value = join(",", local.prod_hosts)
}

output "prod_count" {
  value = length(local.prod_hosts)
}

output "dev_upper" {
  value = join(",", local.dev_upper)
}

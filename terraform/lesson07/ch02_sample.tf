# lesson07 ch02: count によるオンオフ
variable "enable_backup" {
  default = true
}

variable "enable_debug" {
  default = false
}

resource "terraform_data" "backup" {
  count = var.enable_backup ? 1 : 0
  input = "backup-plan"
}

resource "terraform_data" "debug" {
  count = var.enable_debug ? 1 : 0
  input = "debug-agent"
}

# count = 0 のリソースは空リストになります
output "backup_count" {
  value = length(terraform_data.backup)
}

# 「無いかもしれない」ものは try で既定値に倒して参照します
output "backup_name" {
  value = try(terraform_data.backup[0].output, "(none)")
}

output "debug_name" {
  value = try(terraform_data.debug[0].output, "(none)")
}

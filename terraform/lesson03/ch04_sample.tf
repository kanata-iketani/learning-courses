# lesson03 ch04: validation
# condition が false になる値を渡すと error_message を出して失敗します。

variable "env" {
  type    = string
  default = "dev"

  validation {
    condition     = contains(["dev", "stg", "prod"], var.env)
    error_message = "env は dev / stg / prod のいずれかにしてください。"
  }
}

# default の "dev" は条件を満たすので、そのまま apply が通ります

output "current_env" {
  value = var.env
}

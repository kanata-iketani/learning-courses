# validation は variable の中に書く入力チェック。condition が false だと
# error_message を出して apply 前に失敗します。default の "dev" は条件を満たします。
variable "env" {
  type    = string
  default = "dev"

  validation {
    condition     = contains(["dev", "stg", "prod"], var.env)
    error_message = "env は dev / stg / prod のいずれかにしてください。"
  }
}

output "current_env" {
  value = var.env
}

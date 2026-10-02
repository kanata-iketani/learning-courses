# backend "s3" の key は「環境/コンポーネント」でパスを切る流儀が定番です。
# ここでは key の組み立てロジックだけを locals で再現します。
variable "env" {
  default = "stg"
}

variable "component" {
  default = "app"
}

locals {
  # 例: stg/app/terraform.tfstate
  state_key = "${var.env}/${var.component}/terraform.tfstate"
}

output "state_key" {
  value = local.state_key
}

# merge は後の引数が勝つので、共通タグに同名キーがあっても個別指定で上書きされます。
# jsonencode はキーをアルファベット順に並べるため、タグの合成結果を
# 安定した文字列として確認できます(採点にも使えます)。
variable "project" {
  default = "skillax"
}

variable "env" {
  default = "prod"
}

locals {
  name_prefix = "${var.project}-${var.env}"
  common_tags = {
    Project   = var.project
    Env       = var.env
    ManagedBy = "terraform"
  }
  service_name = "${local.name_prefix}-api"
}

output "name" {
  value = local.service_name
}

output "tags" {
  value = jsonencode(merge(local.common_tags, { Name = local.service_name }))
}

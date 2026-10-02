# 命名とタグの定番: name_prefix と common_tags を locals に集約し、
# resource 側では merge で個別タグ(Name など)を足します。
variable "project" {
  default = "app"
}

variable "env" {
  default = "dev"
}

locals {
  name_prefix = "${var.project}-${var.env}"
  common_tags = {
    Project   = var.project
    Env       = var.env
    ManagedBy = "terraform"
  }
}

output "bucket_name" {
  value = "${local.name_prefix}-logs"
}

# jsonencode はキーをアルファベット順に並べるので出力が安定します
output "bucket_tags" {
  value = jsonencode(merge(local.common_tags, { Name = "${local.name_prefix}-logs" }))
}

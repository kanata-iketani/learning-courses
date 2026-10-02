# 組み立てを locals に集約する流儀。name_prefix を一度作れば、
# 以後は local.name_prefix を参照するだけで命名がぶれません。
# locals の中から別の locals を参照するときも local. を使います。
variable "project" {
  type    = string
  default = "skillax"
}

variable "env" {
  type    = string
  default = "stg"
}

locals {
  name_prefix = "${var.project}-${var.env}"
  bucket_name = "${local.name_prefix}-logs"
}

output "bucket_name" {
  value = local.bucket_name
}

output "name_prefix" {
  value = local.name_prefix
}

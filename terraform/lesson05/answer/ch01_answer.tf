variable "service" {
  default = "Web"
}

variable "env" {
  default = "STG"
}

# 入力の大文字小文字に依存しないよう、lower で正規化してから format で組み立てます。
# 名前の組み立てを locals に置くと、複数の output(や実務ではリソース)から再利用できます。
locals {
  bucket = format("%s-%s-logs", lower(var.service), lower(var.env))
}

output "bucket" {
  value = local.bucket
}

output "env_part" {
  value = split("-", local.bucket)[1]
}

output "underscored" {
  value = replace(local.bucket, "-", "_")
}

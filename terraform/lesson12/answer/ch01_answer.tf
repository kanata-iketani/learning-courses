# state list に並ぶのは「型.名前」のアドレスです。実物の state は
# 手で消したり直接編集したりせず、state list / state show で読むのが安全です。
locals {
  addresses = [
    "aws_ecs_service.api",
    "aws_iam_role.task",
    "aws_s3_bucket.logs",
  ]
}

# sort で並びを固定してから join で1本の文字列にします
output "addresses" {
  value = join(", ", sort(local.addresses))
}

output "resource_count" {
  value = length(local.addresses)
}

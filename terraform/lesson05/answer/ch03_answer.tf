variable "common_tags" {
  default = {
    Env     = "prod"
    Project = "skillax"
  }
}

variable "extra_tags" {
  default = {
    Env  = "stg"
    Name = "skillax-api"
  }
}

# merge は「後勝ち」なので、共通タグを先・個別タグを後に書くと個別側が優先されます。
# 実務のタグ付けはほぼこの形(merge(local.common_tags, {...}))で書かれています。
locals {
  tags = merge(var.common_tags, var.extra_tags)
}

output "env" {
  value = local.tags["Env"]
}

output "owner" {
  value = lookup(local.tags, "Owner", "unknown")
}

output "tag_keys" {
  value = join(",", keys(local.tags))
}

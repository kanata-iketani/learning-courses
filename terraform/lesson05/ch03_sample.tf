# lesson05 ch03: merge と lookup
variable "common_tags" {
  default = {
    Env     = "prod"
    Project = "myapp"
  }
}

locals {
  # merge は後勝ち。Env は "stg" に上書きされます
  bucket_tags = merge(var.common_tags, {
    Env  = "stg"
    Name = "myapp-logs"
  })
}

output "env" {
  value = local.bucket_tags["Env"]
}

# lookup はキーが無いときに第3引数の既定値を返します
output "owner" {
  value = lookup(local.bucket_tags, "Owner", "unknown")
}

output "tag_keys" {
  value = join(",", keys(local.bucket_tags))
}

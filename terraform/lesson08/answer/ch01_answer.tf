variable "buckets" {
  default = ["assets", "logs"]
}

# for_each はリストを受け取れないので toset で set に変換します。
# 作られたリソースは「要素の値」がキーのマップになり、index ずれが起きません。
resource "terraform_data" "bucket" {
  for_each = toset(var.buckets)
  input    = format("bucket-%s", each.value)
}

output "bucket_keys" {
  value = join(",", keys(terraform_data.bucket))
}

output "logs" {
  value = terraform_data.bucket["logs"].output
}

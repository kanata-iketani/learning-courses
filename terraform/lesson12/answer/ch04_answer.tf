# alias なしの設定を default というキーで持つと対応表として整理しやすいです。
# cdn には provider = aws.virginia が付いているので、作られる先は
# map の virginia キーの値 us-east-1 です。
locals {
  provider_regions = {
    default  = "ap-northeast-1"
    osaka    = "ap-northeast-3"
    virginia = "us-east-1"
  }
}

output "alias_count" {
  value = length(local.provider_regions)
}

output "aliases" {
  value = join(", ", keys(local.provider_regions))
}

output "cert_region" {
  value = local.provider_regions["virginia"]
}

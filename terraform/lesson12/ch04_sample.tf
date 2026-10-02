# alias とリージョンの対応表を locals で整理します。
# provider = aws.virginia が付いたリソースは us-east-1 に作られます。
locals {
  provider_regions = {
    default  = "ap-northeast-1"
    virginia = "us-east-1"
  }
}

output "default_region" {
  value = local.provider_regions["default"]
}

output "virginia_region" {
  value = local.provider_regions["virginia"]
}

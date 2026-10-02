variable "azs" {
  default = ["ap-northeast-1a", "ap-northeast-1c"]
}

variable "extra_azs" {
  default = ["ap-northeast-1d"]
}

# 連結結果を locals に置けば、length / join / contains のすべてで同じ値を参照できます。
# 実務でも「基本リスト + 環境ごとの追加分」を concat でまとめるパターンをよく見ます。
locals {
  all_azs = concat(var.azs, var.extra_azs)
}

output "all" {
  value = join(",", local.all_azs)
}

output "az_count" {
  value = length(local.all_azs)
}

output "has_1a" {
  value = contains(local.all_azs, "ap-northeast-1a")
}

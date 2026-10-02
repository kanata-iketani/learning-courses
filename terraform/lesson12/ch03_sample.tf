# バージョン制約の意味を locals の対応表で整理します。
locals {
  constraints = {
    "~> 5.67"   = "5.67 以上 6.0 未満(マイナー更新まで許可)"
    "~> 5.67.0" = "5.67.0 以上 5.68.0 未満(パッチ更新のみ許可)"
    ">= 1.5.0"  = "1.5.0 以上なら何でもよい(上限なし)"
  }
}

output "pessimistic_minor" {
  value = local.constraints["~> 5.67"]
}

output "lower_bound_only" {
  value = local.constraints[">= 1.5.0"]
}

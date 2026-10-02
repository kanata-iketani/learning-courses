# 「variable の数と resource の数の比」で流儀を推測するロジックです。

locals {
  # あるモジュールを読解してカウントした結果とします
  input_count    = 14 # variable の数
  resource_count = 1  # resource の数

  # resource が入力より多ければ「厚い」、少なければ「薄い」と推測
  style = local.resource_count > local.input_count ? "thick" : "thin"
}

output "style" {
  value = local.style
}

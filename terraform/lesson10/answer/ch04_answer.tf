locals {
  modules = {
    s3_bucket = { inputs = 14, resources = 1 }  # 入力が多くリソース 1 個 → 薄い
    vpc       = { inputs = 4, resources = 12 }  # 入力が少なくリソース多数 → 厚い
  }

  # マップへの for 式は k(キー), v(値) の 2 変数で回り、キーのアルファベット順になります
  styles = [for k, v in local.modules : "${k}:${v.resources > v.inputs ? "thick" : "thin"}"]
}

output "styles" {
  value = join(", ", local.styles)
}

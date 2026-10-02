# lesson01 ch02: ブロックの解剖
# ブロックは「種別 + ラベル + { 引数 }」でできています。

resource "terraform_data" "web" {
  # 引数は「名前 = 式」。右辺の式にはリテラルや参照を書けます
  input = "block-anatomy"
}

// コメントは # のほかに // も使えます(実務では # が主流)

output "web_input" {
  # 式の例: リソース参照(詳しくは lesson02)
  value = terraform_data.web.output
}

output "block_type" {
  # 式の例: 文字列リテラル
  value = "resource"
}

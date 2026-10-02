# resource ブロックは「種別 resource + ラベル2つ(型と名前)+ 本体」で書きます。
# 本体の「名前 = 式」が引数で、output ブロックはラベル1つです。
resource "terraform_data" "note" {
  input = "HCLは宣言的" # 引数: 名前 = 式
}

output "note" {
  value = terraform_data.note.output
}

output "kind" {
  value = "resource"
}

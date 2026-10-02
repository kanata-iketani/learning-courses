# terraform_data は input に入れた値を output 属性としてそのまま持つ練習用リソースです。
# resource "型" "名前" { ... } が HCL の基本形で、参照は 型.名前.属性 と書きます。
resource "terraform_data" "greeting" {
  input = "Terraformをはじめます"
}

output "greeting" {
  value = terraform_data.greeting.output
}

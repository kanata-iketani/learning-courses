# resource "型" "名前" { ... } が基本形。名前 server はコード内だけの識別子です。
# terraform_data は input の値をそのまま属性 output に持つ練習用リソースです。
resource "terraform_data" "server" {
  input = "web-01"
}

output "server_name" {
  value = terraform_data.server.output
}

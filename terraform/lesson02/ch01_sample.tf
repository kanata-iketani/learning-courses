# lesson02 ch01: resource の基本形
# resource "型" "名前" { 引数 } が基本形です。

resource "terraform_data" "server" {
  # terraform_data は input の値をそのまま属性 output に持ちます
  input = "practice"
}

# 名前(server)はコード内だけの識別子で、参照に使います

output "server_value" {
  value = terraform_data.server.output
}

output "resource_type" {
  value = "terraform_data"
}

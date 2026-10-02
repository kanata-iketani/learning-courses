# lesson01 ch01: はじめての Terraform
# この講座の「▶ 実行」は terraform init → apply → output を一気に実行します。
# terraform_data はクラウド不要の練習用リソースです。

resource "terraform_data" "hello" {
  input = "Hello, Terraform!"
}

# output は apply 後に値を表示するブロックです(採点にも使います)
output "message" {
  value = terraform_data.hello.output
}

output "tool" {
  value = "IaC"
}

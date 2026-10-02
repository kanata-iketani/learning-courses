# 参照は 型.名前.属性。ここでは terraform_data.origin.output です。
# 参照を書くと Terraform が「origin を先に作る」という依存関係を自動で組みます。
resource "terraform_data" "origin" {
  input = "参照元"
}

output "from_resource" {
  value = terraform_data.origin.output
}

output "ref_style" {
  value = "型.名前.属性"
}

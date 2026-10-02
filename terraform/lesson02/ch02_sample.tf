# lesson02 ch02: リソース参照
# 「型.名前.属性」で他のリソースの値を使えます。

resource "terraform_data" "origin" {
  input = "origin-value"
}

output "from_resource" {
  # 参照を書いた時点で origin への依存関係が自動でできます
  value = terraform_data.origin.output
}

output "from_literal" {
  # こちらはただのリテラル。参照ではありません
  value = "origin-value"
}

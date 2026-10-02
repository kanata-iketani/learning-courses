# lesson02 ch03: 参照のチェーン
# base → middle → last の順で自動的に作られます。

resource "terraform_data" "base" {
  input = "base-v1"
}

resource "terraform_data" "middle" {
  # base への参照。base が先に作られます
  input = terraform_data.base.output
}

resource "terraform_data" "last" {
  # middle への参照。チェーンは何段でも OK
  input = terraform_data.middle.output
}

output "chain_result" {
  value = terraform_data.last.output
}

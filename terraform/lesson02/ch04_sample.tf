# lesson02 ch04: data ソースの読み方(演習は terraform_data で代用)
# 実務の data "aws_..." は「既存のものを読むだけ」のブロックです。

# ここでは registry を「既存の共有値」に見立てます
resource "terraform_data" "registry" {
  input = "shared-config-v2"
}

resource "terraform_data" "consumer" {
  # 読み取った値を使う側。data 参照と同じ「読んで使う」構図です
  input = terraform_data.registry.output
}

output "consumed" {
  value = terraform_data.consumer.output
}

output "verb" {
  value = "read-only"
}

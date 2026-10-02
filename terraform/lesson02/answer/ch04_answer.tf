# 実務の data ソースは「作らずに読む」ブロック。ここでは registry を
# 既存の値に見立てて、参照で読み取る構図だけを再現しています。
# bool 値はクォートなしで true / false と書きます。
resource "terraform_data" "registry" {
  input = "ami-12345678"
}

output "ami_id" {
  value = terraform_data.registry.output
}

output "readonly" {
  value = true
}

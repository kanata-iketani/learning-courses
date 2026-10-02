# module ブロックでローカルモジュールを呼び出します。
# エディタでは「# === file: パス ===」の区切り行から下が別ファイルになります。

module "hello" {
  source = "./modules/greet" # ./ 始まり = ローカルモジュール
  name   = "terraform"
}

# モジュールの output は module.<呼び出し名>.<output名> で参照します
output "message" {
  value = module.hello.message
}

# === file: modules/greet/main.tf ===
# ここから下は modules/greet/main.tf として保存されます

variable "name" {
  type = string
}

output "message" {
  value = "hello, ${var.name}"
}

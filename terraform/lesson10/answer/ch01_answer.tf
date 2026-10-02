# source が ./ で始まるのでローカルモジュール。実体は modules/greet/main.tf です。
# name = "module" は、モジュール側の variable "name" への入力になります。
module "welcome" {
  source = "./modules/greet"
  name   = "module"
}

output "greeting" {
  value = module.welcome.message
}

# === file: modules/greet/main.tf ===
variable "name" {
  type = string
}

output "message" {
  value = "hello, ${var.name}"
}

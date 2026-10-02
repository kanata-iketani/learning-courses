# backend の bucket / key は直書きされていることが多いですが、
# 命名規則としては「project-tfstate」「env/component/terraform.tfstate」の
# 組み立てです。この規則が読めると state の置き場所を推測できます。
variable "project" {
  default = "skillax"
}

variable "env" {
  default = "prod"
}

variable "component" {
  default = "network"
}

output "bucket" {
  value = "${var.project}-tfstate"
}

output "state_key" {
  value = "${var.env}/${var.component}/terraform.tfstate"
}

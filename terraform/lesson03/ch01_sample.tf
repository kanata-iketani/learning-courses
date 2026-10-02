# lesson03 ch01: variable と var.
# variable は外から値を受け取る入力口。default があれば入力なしで動きます。

variable "project" {
  type    = string
  default = "myapp"
}

variable "region" {
  type    = string
  default = "ap-northeast-1"
}

output "project_name" {
  # 参照は var.名前
  value = var.project
}

output "region_name" {
  value = var.region
}

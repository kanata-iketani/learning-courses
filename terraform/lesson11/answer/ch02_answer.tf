variable "env" {
  type    = string
  default = "stg"
}

# tfvars 方式なら -var-file、workspace 方式なら terraform.workspace で
# env の値が切り替わり、この 3 つの条件式の結果がまとめて変わります。
output "log_level" {
  value = var.env == "prod" ? "warn" : "debug"
}

output "min_capacity" {
  value = var.env == "prod" ? 4 : 1
}

output "retention_days" {
  value = var.env == "prod" ? 365 : 7
}

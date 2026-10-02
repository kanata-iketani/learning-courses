# object 型は関連する設定の束。実務の variables.tf で多用されます。
# 属性参照は var.db.name のようにドットでつなぎます。
variable "db" {
  type = object({
    name = string
    port = number
  })
  default = {
    name = "app-db"
    port = 5432
  }
}

output "db_name" {
  value = var.db.name
}

output "db_port" {
  value = var.db.port
}

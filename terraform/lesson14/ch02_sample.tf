# count 時代の [0] から for_each のキーへ移行した「痕跡」の実例です。
variable "names" {
  default = ["blue"]
}

resource "terraform_data" "web" {
  for_each = toset(var.names)
  input    = "web-${each.key}"
}

# 以前 count だったころのアドレスからの付け替えを宣言(新規 apply では何もしない)
moved {
  from = terraform_data.web[0]
  to   = terraform_data.web["blue"]
}

output "web_addresses" {
  value = join(", ", [for k in keys(terraform_data.web) : "terraform_data.web[\"${k}\"]"])
}

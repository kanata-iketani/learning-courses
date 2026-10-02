# lesson07 ch01: count と count.index
variable "replicas" {
  default = 3
}

resource "terraform_data" "web" {
  count = var.replicas
  # count.index は 0 始まり。+1 して 1 始まりの連番にするのが定番です
  input = format("web-%02d", count.index + 1)
}

# count 付きリソースはリストになるので [0] で個別参照できます
output "first" {
  value = terraform_data.web[0].output
}

# [*] (splat) で全要素の属性をまとめて取り出せます
output "all" {
  value = join(",", terraform_data.web[*].output)
}

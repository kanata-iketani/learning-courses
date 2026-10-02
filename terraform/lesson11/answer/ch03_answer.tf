variable "steps" {
  type    = list(string)
  default = ["backend", "provider", "variables", "main"]
}

# for 式の i はインデックス(0 始まり)なので、表示用に i + 1 して 1 始まりにします。
# この並び(backend → provider → variables → main)が初見リポジトリを読む順です。
locals {
  numbered = [for i, s in var.steps : "${i + 1}:${s}"]
}

output "checklist" {
  value = join(", ", local.numbered)
}

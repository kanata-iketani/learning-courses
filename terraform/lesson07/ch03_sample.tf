# lesson07 ch03: index のずれを観察する
variable "members" {
  default = ["ito", "kato", "sato"]
}

resource "terraform_data" "member" {
  count = length(var.members)
  # 「index:名前」の対応を記録しておきます
  input = format("%d:%s", count.index, var.members[count.index])
}

# ito は [0]、kato は [1]、sato は [2] に対応しています。
# ここから kato を消すと sato が [1] に繰り上がり、作り直しの対象になります
output "pairs" {
  value = join(" ", terraform_data.member[*].output)
}

output "member_count" {
  value = length(terraform_data.member)
}

variable "owner" {
  default = ""
}

variable "tags" {
  type = map(string)
  default = {
    Team = "core"
  }
}

# coalesce は "" も「値なし」とみなすので、未設定時のフォールバックに便利です。
# try はマップにキーが無くてもエラーで止めず既定値へ倒す、防御的な定番の書き方です。
output "owner" {
  value = coalesce(var.owner, "platform")
}

output "team" {
  value = try(var.tags["Team"], "none")
}

output "cost_center" {
  value = try(var.tags["CostCenter"], "none")
}

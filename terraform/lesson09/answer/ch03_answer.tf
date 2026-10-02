variable "rules" {
  type    = list(string)
  default = ["https", "ssh"]
}

# 「件数が可変・多数なら dynamic、固定少数なら直書き」という実務の判断を
# length + 条件式で表しています。2 件なので static(直書きで十分)になります。
output "decision" {
  value = length(var.rules) >= 3 ? "dynamic" : "static"
}

output "rule_count" {
  value = length(var.rules)
}

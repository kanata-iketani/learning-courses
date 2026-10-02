# 流儀1(jsonencode 直書き)のポリシー組み立てを locals で再現します。
# jsonencode は HCL のオブジェクトを JSON 文字列に変換します(キーはソートされる)。
locals {
  read_policy = {
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:GetObject"]
      Resource = "arn:aws:s3:::app-logs/*"
    }]
  }
}

output "policy_json" {
  value = jsonencode(local.read_policy)
}

output "statement_count" {
  value = length(local.read_policy.Statement)
}

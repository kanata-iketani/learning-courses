# policy_document の effect / actions / resources は、jsonencode 流儀では
# Effect / Action / Resource という大文字キーに対応します。
# jsonencode はキー順ソートで出力が決定的なので、2流儀の比較にも便利です。
locals {
  policy = {
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["s3:GetObject", "s3:ListBucket"]
      Resource = [
        "arn:aws:s3:::skillax-prod-logs",
        "arn:aws:s3:::skillax-prod-logs/*",
      ]
    }]
  }
}

output "action_count" {
  value = length(local.policy.Statement[0].Action)
}

output "policy" {
  value = jsonencode(local.policy)
}

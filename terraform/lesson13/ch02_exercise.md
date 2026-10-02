# lesson13 ch02 演習: IAMポリシーの2流儀

流儀2(`data "aws_iam_policy_document"`)で書かれた次のポリシーを、流儀1(jsonencode 直書き)に書き換えたときの JSON を出力してください。

```hcl
data "aws_iam_policy_document" "logs_read" {
  statement {
    effect    = "Allow"
    actions   = ["s3:GetObject", "s3:ListBucket"]
    resources = [
      "arn:aws:s3:::skillax-prod-logs",
      "arn:aws:s3:::skillax-prod-logs/*",
    ]
  }
}
```

locals にポリシーをオブジェクトで組み立ててください(`Version = "2012-10-17"`、`Statement` は `Effect` / `Action` / `Resource` キーを持つ1要素のリスト)。そのうえで

- output `action_count`: Action の数
- output `policy`: ポリシー全体を `jsonencode()` した文字列

を出力してください。

**期待出力**

```text
action_count = 2
policy = "{\"Statement\":[{\"Action\":[\"s3:GetObject\",\"s3:ListBucket\"],\"Effect\":\"Allow\",\"Resource\":[\"arn:aws:s3:::skillax-prod-logs\",\"arn:aws:s3:::skillax-prod-logs/*\"]}],\"Version\":\"2012-10-17\"}"
```

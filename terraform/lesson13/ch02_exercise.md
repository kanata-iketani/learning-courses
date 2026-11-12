# lesson13 ch02 演習: IAMポリシーの2流儀

流儀2(`data "aws_iam_policy_document"`)で書かれた次のポリシーを、流儀1(jsonencode 直書き)に書き換えたときの JSON を出力してください。

```hcl
data "aws_iam_policy_document" "logs_read" {
  statement {
    effect    = "Allow"
    actions   = ["s3:GetObject", "s3:ListBucket"]
    resources = [
      "arn:aws:s3:::myapp-prod-logs",
      "arn:aws:s3:::myapp-prod-logs/*",
    ]
  }
}
```

(読み方: `s3:ListBucket` はバケットの中のファイル一覧を取る操作で、対象はバケットそのもの(`arn:aws:s3:::myapp-prod-logs`)です。`s3:GetObject` はファイルを読む操作で、対象はバケットの中のファイル(`.../*`)です。操作ごとに対象が違うので、resources に2つの ARN が並んでいます)

locals にポリシーをオブジェクトで組み立ててください(`Version = "2012-10-17"`、`Statement` は `Effect` / `Action` / `Resource` キーを持つ1要素のリスト)。そのうえで

- output `action_count`: Action の数
- output `policy`: ポリシー全体を `jsonencode()` した文字列

を出力してください。

(ヒント: `actions` → `Action`、`resources` → `Resource` のように大文字のキーに書き換え、値のリストはそのまま使います。Action の数は `local.policy.Statement[0].Action` で1つ目のステートメントの Action リストを取り出し、`length()` で数えます。`[0]` はリストの1つ目(0から数える)です)

**期待出力**

```text
action_count = 2
policy = "{\"Statement\":[{\"Action\":[\"s3:GetObject\",\"s3:ListBucket\"],\"Effect\":\"Allow\",\"Resource\":[\"arn:aws:s3:::myapp-prod-logs\",\"arn:aws:s3:::myapp-prod-logs/*\"]}],\"Version\":\"2012-10-17\"}"
```

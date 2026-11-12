# lesson08 ch01 演習: setでfor_each — each.value

variable `buckets`(default `["assets", "logs"]`)を宣言し、`terraform_data` リソース `bucket` を `for_each = toset(var.buckets)` で作成、`input` には `bucket-要素名`(例: `bucket-logs`)を設定してください。そのうえで次の2つを出力してください。

- output `bucket_keys`: 作られたリソースのキー一覧を `,` 区切りで join した文字列
- output `logs`: キー `"logs"` のリソースの `output` 属性

(ヒント: 今の要素は `each.value`、`bucket-要素名` は `format("bucket-%s", each.value)` で作れます。キー一覧は `keys(terraform_data.bucket)`、それを `,` でつなぐのは `join(",", ...)` です。キーで1つ取り出すときは `terraform_data.bucket["logs"]` と書きます)

**期待出力**

```text
bucket_keys = "assets,logs"
logs = "bucket-logs"
```

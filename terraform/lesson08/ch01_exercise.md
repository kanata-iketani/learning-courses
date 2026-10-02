# lesson08 ch01 演習: setでfor_each — each.value

variable `buckets`(default `["assets", "logs"]`)を宣言し、`terraform_data` リソース `bucket` を `for_each = toset(var.buckets)` で作成、`input` には `bucket-要素名`(例: `bucket-logs`)を設定してください。そのうえで次の2つを出力してください。

- output `bucket_keys`: 作られたリソースのキー一覧を `,` 区切りで join した文字列
- output `logs`: キー `"logs"` のリソースの `output` 属性

**期待出力**

```text
bucket_keys = "assets,logs"
logs = "bucket-logs"
```

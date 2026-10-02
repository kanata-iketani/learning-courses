# lesson04 ch04 演習: varとlocalsの使い分け・命名の流儀

locals 集約スタイルで名前を組み立てます。

1. variable `project` を定義: `type` は `string`、`default` は `"skillax"`
2. variable `env` を定義: `type` は `string`、`default` は `"stg"`
3. locals で `name_prefix = "${var.project}-${var.env}"` と、それを使った `bucket_name = "${local.name_prefix}-logs"` を定義
4. output `bucket_name` で `local.bucket_name` を、output `name_prefix` で `local.name_prefix` を表示

**期待出力**

```text
bucket_name = "skillax-stg-logs"
name_prefix = "skillax-stg"
```

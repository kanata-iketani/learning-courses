# lesson04 ch02 演習: 文字列補間と演算子

variable と補間で名前を組み立てます。

1. variable `app` を定義: `type` は `string`、`default` は `"billing"`
2. variable `env` を定義: `type` は `string`、`default` は `"prod"`
3. locals で `name = "${var.app}-${var.env}"` と `total_capacity = 4 * 3` を定義
4. output `resource_name` で `local.name` を、output `total_capacity` で `local.total_capacity` を表示

**期待出力**

```text
resource_name = "billing-prod"
total_capacity = 12
```

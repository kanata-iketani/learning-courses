# lesson04 ch03 演習: 条件式 cond ? a : b

環境によって値を切り替えます。

1. variable `env` を定義: `type` は `string`、`default` は `"prod"`
2. locals で `instance_type` を定義: `var.env` が `"prod"` なら `"large"`、それ以外なら `"small"` になる条件式
3. output `instance_type` で `local.instance_type` を、output `is_production` で `var.env == "prod"` の結果を表示

**期待出力**

```text
instance_type = "large"
is_production = true
```

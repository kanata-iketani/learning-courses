# lesson04 ch03 演習: 条件式 cond ? a : b

環境によって値を切り替えます。

1. variable `env` を定義: `type` は `string`、`default` は `"prod"`
2. locals で `instance_type` を定義: `var.env` が `"prod"` なら `"large"`、それ以外なら `"small"` になる条件式
3. output `instance_type` で `local.instance_type` を、output `is_production` で `var.env == "prod"` の結果を表示

(ヒント: 条件式は `条件 ? 真のときの値 : 偽のときの値` の順に書きます。`var.env == "prod"` は比較の結果 `true` / `false` になる式なので、そのまま `value = ` の右に書けます)

**期待出力**

```text
instance_type = "large"
is_production = true
```

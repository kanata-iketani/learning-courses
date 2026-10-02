# lesson05 ch04 演習: try・coalesce・jsonencode — 壊れにくい書き方

variable `owner`(default `""`)と `tags`(type `map(string)`、default `{ Team = "core" }`)を宣言し、次の3つを出力してください。

- output `owner`: `coalesce` を使い、`var.owner` が空文字なら `"platform"` にフォールバックした値
- output `team`: `try` を使って `var.tags["Team"]` を取り出す。失敗したら `"none"`
- output `cost_center`: `try` を使って `var.tags["CostCenter"]` を取り出す。失敗したら `"none"`

**期待出力**

```text
cost_center = "none"
owner = "platform"
team = "core"
```

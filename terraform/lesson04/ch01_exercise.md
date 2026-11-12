# lesson04 ch01 演習: localsとlocal.

variable と locals を組み合わせます。

1. variable `team` を定義: `type` は `string`、`default` は `"sre"`
2. locals ブロックで `retention_days = 30` を定義
3. output `owner_team` で `var.team` を、output `retention` で `local.retention_days` を表示

(ヒント: locals ブロックはラベルなしで `locals { ... }` と書きます。参照は `locals.` ではなく `local.`(単数形)です。数値は引用符なしで書くと、出力も `30` のように引用符なしで表示されます)

**期待出力**

```text
owner_team = "sre"
retention = 30
```

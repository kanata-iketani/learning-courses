# lesson10 ch04 演習: 薄いモジュールvs厚いモジュール

2 つのモジュールの読解メモから、それぞれの流儀を判定してください。

1. locals にマップ `modules` を定義する: キー `s3_bucket` は `{ inputs = 14, resources = 1 }`、キー `vpc` は `{ inputs = 4, resources = 12 }`
2. for 式で各モジュールを `"名前:判定"` 形式にする。判定は `resources` が `inputs` より大きければ `"thick"`、そうでなければ `"thin"`
3. output `styles` で `join(", ", ...)` した結果を表示する(マップの for 式はキーのアルファベット順に回ります)

**期待出力**

```text
styles = "s3_bucket:thin, vpc:thick"
```

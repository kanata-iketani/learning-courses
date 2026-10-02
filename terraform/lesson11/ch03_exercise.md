# lesson11 ch03 演習: 初見のリポジトリを読む手順

読解チェックリストを 1 行の文字列に整形してください。

1. `variable "steps"` を `list(string)` 型、default `["backend", "provider", "variables", "main"]` で定義する
2. インデックス付き for 式で各手順を `"1:backend"` 形式(番号は 1 始まり)にする
3. output `checklist` で `join(", ", ...)` した結果を表示する

**期待出力**

```text
checklist = "1:backend, 2:provider, 3:variables, 4:main"
```

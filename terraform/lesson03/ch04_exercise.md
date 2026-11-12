# lesson03 ch04 演習: tfvarsと優先順位・validation

variable `env` を定義してください。

- `type` は `string`、`default` は `"dev"`
- validation ブロックを付け、`condition` に `contains(["dev", "stg", "prod"], var.env)`、`error_message` に好きなメッセージ(文字列)を設定

さらに output `current_env` で `var.env` を表示してください。

(ヒント: `validation { ... }` は variable ブロックの `{ }` の中に書きます。`error_message` は `"..."` で囲んだ文字列にします。default の `"dev"` は条件を満たすので、apply はそのまま通ります)

**期待出力**

```text
current_env = "dev"
```

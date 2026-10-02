# lesson03 ch04 演習: tfvarsと優先順位・validation

variable `env` を定義してください。

- `type` は `string`、`default` は `"dev"`
- validation ブロックを付け、`condition` に `contains(["dev", "stg", "prod"], var.env)`、`error_message` に好きなメッセージ(文字列)を設定

さらに output `current_env` で `var.env` を表示してください。

**期待出力**

```text
current_env = "dev"
```

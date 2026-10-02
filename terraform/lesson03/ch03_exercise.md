# lesson03 ch03 演習: object型と実務のvariables.tf

variable `db` を object 型で定義してください。

- `type` は `object({ name = string, port = number })`
- `default` は `{ name = "app-db", port = 5432 }`

さらに output `db_name` で `var.db.name` を、output `db_port` で `var.db.port` を表示してください。

**期待出力**

```text
db_name = "app-db"
db_port = 5432
```

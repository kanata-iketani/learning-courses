# lesson06 ch02 演習: mapを作るfor式 — {for k, v in ...}

variable `sizes`(default `{ api = "t3.medium", web = "t3.small" }`)を宣言し、for式で「キーはそのまま、値を `キー:値` という文字列にした」マップを locals に作って、次の3つを出力してください。

- output `label_keys`: 新しいマップのキー一覧を `,` 区切りで join した文字列
- output `label_values`: 新しいマップの値一覧(values)を半角スペース区切りで join した文字列
- output `web`: 新しいマップの `"web"` キーの値

(ヒント: 値は文字列補間で `"${k}:${v}"` と組み立てられます。マップのキー一覧は `keys`、値の一覧は `values`(lesson05)で、どちらもキーのアルファベット順のリストになります。半角スペース区切りは `join(" ", ...)` です。マップの値は `local.名前["web"]` で取り出せます)

**期待出力**

```text
label_keys = "api,web"
label_values = "api:t3.medium web:t3.small"
web = "web:t3.small"
```

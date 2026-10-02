# lesson08 ch02 演習: mapでfor_each — each.keyとeach.value

variable `instances`(default `{ api = "t3.medium", web = "t3.small" }`)を宣言し、`terraform_data` リソース `instance` を `for_each = var.instances` で作成、`input` には `format("%s=%s", each.key, each.value)` を設定してください。そのうえで次の2つを出力してください。

- output `api`: キー `"api"` のリソースの `output` 属性
- output `instance_keys`: 作られたリソースのキー一覧を `,` 区切りで join した文字列

**期待出力**

```text
api = "api=t3.medium"
instance_keys = "api,web"
```

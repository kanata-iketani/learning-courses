# lesson08 ch03 演習: for_eachリソースの参照 — [キー]とvalues()

variable `topics`(default `["audit", "mail", "sync"]`)を宣言し、`terraform_data` リソース `topic` を `for_each = toset(var.topics)` で作成、`input` には `topic-要素名` を設定してください。そのうえで次の2つを出力してください。

- output `all_topics`: `values()` と splat を使い、全リソースの `output` 属性を `,` 区切りで join した文字列
- output `mail`: キー `"mail"` のリソースの `output` 属性

**期待出力**

```text
all_topics = "topic-audit,topic-mail,topic-sync"
mail = "topic-mail"
```

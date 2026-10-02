# lesson07 ch02 演習: count = 条件 ? 1 : 0 — オンオフパターン

variable `enable_logging`(default `true`)と `enable_monitoring`(default `false`)を宣言し、`terraform_data` リソース `logging`(input は `"logging-on"`)と `monitoring`(input は `"monitoring-on"`)を、それぞれのフラグによる `条件 ? 1 : 0` パターンで作成してください。そのうえで次の3つを出力してください。

- output `logging`: `try` を使い、logging リソースがあればその `output` 属性、無ければ `"off"`
- output `logging_count`: logging リソースの個数
- output `monitoring`: `try` を使い、monitoring リソースがあればその `output` 属性、無ければ `"off"`

**期待出力**

```text
logging = "logging-on"
logging_count = 1
monitoring = "off"
```

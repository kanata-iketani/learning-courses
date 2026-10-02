# lesson06 ch03 演習: ifでフィルタするfor式

variable `buckets`(default `["logs-prod", "logs-dev", "assets-prod", "tmp-dev"]`)を宣言し、for式の `if` で `-prod` で終わるものだけを残したリストを locals に作って、次の2つを出力してください。

- output `prod_buckets`: 残ったリストを `,` 区切りで join した文字列
- output `prod_count`: 残った要素数

**期待出力**

```text
prod_buckets = "logs-prod,assets-prod"
prod_count = 2
```

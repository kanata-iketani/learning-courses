# lesson06 ch03 演習: ifでフィルタするfor式

variable `buckets`(default `["logs-prod", "logs-dev", "assets-prod", "tmp-dev"]`)を宣言し、for式の `if` で `-prod` で終わるものだけを残したリストを locals に作って、次の2つを出力してください。

- output `prod_buckets`: 残ったリストを `,` 区切りで join した文字列
- output `prod_count`: 残った要素数

(ヒント: `endswith(文字列, "-prod")` は、文字列が `-prod` で終わっていれば true を返します。`if` は for式の `: 式` の後ろに置きます。今回は変換しないので `: b` のように取り出した要素をそのまま書きます)

**期待出力**

```text
prod_buckets = "logs-prod,assets-prod"
prod_count = 2
```

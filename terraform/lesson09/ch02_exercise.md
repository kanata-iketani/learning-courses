# lesson09 ch02 演習: contentとiterator

text の dynamic ブロックが次のルールリストを受け取ったときに生成する内容を、for 式で再現してください。

1. `variable "ingress_rules"` を `list(object({ port = number, cidr = string }))` 型で定義し、default に `{ port = 22, cidr = "10.0.0.0/8" }` と `{ port = 443, cidr = "0.0.0.0/0" }` の 2 件を入れる
2. for 式で各ルールを `"22 from 10.0.0.0/8"` 形式の文字列にする
3. output `ingress` で `join(", ", ...)` した結果を表示する

**期待出力**

```text
ingress = "22 from 10.0.0.0/8, 443 from 0.0.0.0/0"
```

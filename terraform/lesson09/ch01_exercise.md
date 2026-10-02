# lesson09 ch01 演習: dynamicブロックの読み方

text の dynamic ブロックが `var.allowed_ports = [22, 80, 443]` を受け取ったとき、生成される ingress ルールを for 式で再現してください。

1. `variable "allowed_ports"` を `list(number)` 型、default `[22, 80, 443]` で定義する
2. locals の for 式で、各ポートを `format("%d-%d/tcp", p, p)` の形式の文字列にする
3. output `rules` で `join(", ", ...)` した結果を表示する

**期待出力**

```text
rules = "22-22/tcp, 80-80/tcp, 443-443/tcp"
```

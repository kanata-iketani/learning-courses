# lesson13 ch03 演習: セキュリティグループのingress列挙

次の SG 定義を読み、生成される ingress ルールを for 式で言語化してください。

```hcl
variable "ingress_ports" {
  default = [80, 443, 8080]
}

resource "aws_security_group" "app" {
  name = "app-sg"

  dynamic "ingress" {
    for_each = var.ingress_ports
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/8"]
    }
  }
}
```

variable `ingress_ports`(default `[80, 443, 8080]`)を定義し、

- output `rule_count`: 生成されるルールの数
- output `rules`: 各ポートを `allow tcp/<port> from 10.0.0.0/8` の形にして `", "` で連結

を出力してください。

(ヒント: dynamic はリストの要素ごとに ingress ブロックを1つ作るので、ルールの数はリストの長さと同じです。`[for p in リスト : "...${p}..."]` の形の for 式(lesson06)で文字列のリストを作り、`length()` で数え、`join(", ", ...)` でつなぎます。`<port>` はポート番号が入る場所という意味です)

**期待出力**

```text
rule_count = 3
rules = "allow tcp/80 from 10.0.0.0/8, allow tcp/443 from 10.0.0.0/8, allow tcp/8080 from 10.0.0.0/8"
```

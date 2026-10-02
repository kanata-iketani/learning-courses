# Lesson 09 dynamicブロック

実務の Terraform で必ず出会う `dynamic` ブロックを読めるようになるレッスンです。セキュリティグループの ingress 列挙など実務風の AWS コードを読解し、演習ではその繰り返しロジックを lesson06 で学んだ for 式と locals で再現します。

## ch01 dynamicブロックの読み方

**dynamic ブロック**(リソース内のネストブロックを for_each で量産する構文)は、実務のセキュリティグループ定義で頻出します。**ネストブロック**(`ingress` のように resource の中に入れ子で書くブロック)は count や for_each 引数では増やせないため、dynamic を使います。`dynamic "ingress"` は「ingress ブロックを繰り返し生成する」という意味で、各要素はブロック名と同じ変数 `ingress.value` で参照します。🟡 「for_each で回っているのは引数ではなくブロックそのもの」と読み替えられれば、実務コードの大半は読めます。

```hcl
resource "aws_security_group" "app" {
  name = "app"

  dynamic "ingress" {
    for_each = var.allowed_ports # [80, 443]
    content {
      from_port = ingress.value
      to_port   = ingress.value
      protocol  = "tcp"
    }
  }
}
```

## ch02 contentとiterator

dynamic の中の **content ブロック**(生成される 1 ブロック分の中身を書く場所)には、通常のブロックと同じ引数を書きます。**iterator**(ループ変数の名前を変える引数)を指定すると、既定の「ブロック名と同じ変数」を別名にできます。for_each にオブジェクトのリストを渡す実務コードでは、`rule.value.port` のように「変数名.value.属性名」の形で読みます。🟡 iterator があるコードでは「どの変数がループ 1 周分を指すか」を最初に確認しましょう。

```hcl
dynamic "ingress" {
  for_each = var.ingress_rules # [{ port = 80, cidr = "10.0.0.0/16" }, ...]
  iterator = rule              # 変数名を ingress → rule に変更
  content {
    from_port   = rule.value.port
    to_port     = rule.value.port
    cidr_blocks = [rule.value.cidr]
  }
}
```

## ch03 dynamicの使いどころと使いすぎ問題

dynamic が向くのは「ルールの件数が variable や環境によって変わる」場合だけです。固定の 2〜3 個なら、ブロックをそのまま並べて書くほうが読みやすく、plan の差分も追いやすくなります。実務レビューでは「dynamic の中に dynamic」のようなネストは可読性が大きく落ちるため避けられる傾向があり、HashiCorp のスタイルガイドも dynamic の乱用を戒めています。⚪ 読解時は「この dynamic は可変件数だから必要なのか、単に短く書きたかっただけか」を判断できれば十分です。

```hcl
# 固定 2 個なら直書きのほうが読みやすい
ingress {
  from_port = 80
  to_port   = 80
}
ingress {
  from_port = 443
  to_port   = 443
}
```

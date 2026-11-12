# Lesson 09 dynamicブロック

実務の Terraform で必ず出会う `dynamic` ブロックを読めるようになるレッスンです。セキュリティグループの ingress 列挙など実務風の AWS コードを読解し、演習ではその繰り返しロジックを lesson06 で学んだ for 式と locals で再現します。

## ch01 dynamicブロックの読み方

### 基礎の基礎: セキュリティグループと ingress

このレッスンの例は、AWS の**セキュリティグループ**(サーバーへの通信を「どこから・どのポートなら許可するか」を決めるルールの集まり)です。読むために必要な用語を先に押さえます。

| 用語 | 意味 |
|---|---|
| **ポート** | 1台のサーバーの中で通信の行き先を区別する番号。Web は 80(HTTP)と 443(HTTPS)、サーバーへのリモートログイン(SSH)は 22 が定番 |
| **ingress** | 外からサーバーへ**入ってくる**通信の許可ルール(反対の、出ていく通信は egress) |
| `from_port` / `to_port` | 許可するポートの範囲の始まりと終わり。80 だけ許可するなら両方 80 |
| `protocol = "tcp"` | 通信の方式。Web や SSH は **TCP**(相手と接続してから確実に届ける通信方式) |
| **CIDR** | `10.0.0.0/16` のように、IP アドレスの範囲を表す書き方。`0.0.0.0/0` は「すべてのアドレス」 |

### ネストブロックとは

セキュリティグループでは、許可ルール1つを `ingress { ... }` というブロックで書きます。このように resource の中に入れ子で書くブロックを**ネストブロック**と呼びます。80 と 443 を許可するなら、ingress ブロックを2つ並べます。

```hcl
resource "aws_security_group" "app" {
  name = "app"                   # セキュリティグループの名前

  ingress {                      # ルール1つ目: 80 番を許可
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # どこからでも
  }
  ingress {                      # ルール2つ目: 443 番を許可
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

lesson07・08 の count や for_each は、**resource ブロックそのもの**を増やす道具でした。resource の中にあるネストブロックは count や for_each 引数では増やせません。そこで使うのが dynamic です。

### dynamic ブロック

**dynamic ブロック**(リソース内のネストブロックを for_each で量産する構文)は、実務のセキュリティグループ定義で頻出します。上の2つの ingress は、次のように書いても同じ意味になります。

```hcl
resource "aws_security_group" "app" {
  name = "app"

  dynamic "ingress" {              # ingress ブロックを繰り返し生成する
    for_each = var.allowed_ports   # [80, 443] の要素ごとに1つ作る
    content {                      # 生成する ingress 1つ分の中身
      from_port   = ingress.value  # 今の要素(80 や 443)
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]  # どこからでも
    }
  }
}
```

| 部分 | 意味 |
|---|---|
| `dynamic "ingress"` | 「`ingress` ブロックを繰り返し生成する」という宣言。ラベルには生成したいブロックの名前を書く |
| `for_each = var.allowed_ports` | 回す集まり。ここは lesson08 と違い、list をそのまま渡せる |
| `content { ... }` | 生成される ingress ブロック1つ分の中身(ch02 で詳しく見ます) |
| `ingress.value` | 今の要素の値。各要素は**ブロック名と同じ変数**(ここでは `ingress`)で参照する |

`var.allowed_ports = [80, 443]` なら、content が2回生成され、`ingress.value` は1回目が 80、2回目が 443 になります。

### 本当に同じになるか確かめる

AWS プロバイダ(AWS を操作するためのプラグイン。lesson12)を使って、ingress を2つ直書きしたコードと、dynamic で書いたコードの plan を比べると、出力は1文字も違わず一致しました。plan の ingress 部分の抜粋です。

```text
      + ingress                = [
          + {
              + cidr_blocks      = [
                  + "0.0.0.0/0",
                ]
              + from_port        = 443
              + protocol         = "tcp"
              + to_port          = 443
              ...
            },
          + {
              + cidr_blocks      = [
                  + "0.0.0.0/0",
                ]
              + from_port        = 80
              + protocol         = "tcp"
              + to_port          = 80
              ...
            },
        ]
```

443 が 80 より先に表示されているのは、セキュリティグループの ingress ルールが順序を持たない集まり(set)として扱われるためで、書いた順とは関係ありません。また plan には dynamic という言葉は出てきません。dynamic は「書き方の省略」で、Terraform が展開した結果は普通の ingress ブロックの並びです。

🟡 「for_each で回っているのは引数ではなくブロックそのもの」と読み替えられれば、実務コードの大半は読めます。

### サンプルと演習の考え方

この講座の実行環境は AWS につながらないため、dynamic そのものは動かせません。そこでサンプルと演習では、dynamic が生成するルールを lesson06 の for 式で「見える化」します。

```hcl
locals {
  ports = [80, 443]
  rules = [for p in local.ports : format("%d-%d/tcp", p, p)]  # 各ポートを "80-80/tcp" 形式に
}
```

- `[for p in local.ports : ...]` は「`local.ports` の要素を1つずつ `p` に入れ、`:` の右の式で作った値を並べたリスト」です(lesson06)。dynamic の `ingress.value` が、for 式の `p` に当たります
- `format("%d-%d/tcp", p, p)` の `%d` は数値を入れる場所です(`%s` の数値版)。`from_port-to_port/protocol` の形の文字列になります

実行結果です。

```text
rule_count = 2
rules = "80-80/tcp, 443-443/tcp"
```

## ch02 contentとiterator

### content ブロック

dynamic の中の **content ブロック**(生成される 1 ブロック分の中身を書く場所)には、通常のブロックと同じ引数を書きます。ch01 で見た直書きの `ingress { ... }` の `{ }` の中身を、そのまま content の中に移すイメージです。違うのは、要素ごとに変わる値を `ingress.value` のような変数で書く点だけです。

dynamic の中で使える変数は次の2つです(変数名は既定ではブロック名と同じ)。

| 変数 | 中身 | `for_each = [80, 443]` の2回目 |
|---|---|---|
| `ingress.value` | 今の要素の値 | `443` |
| `ingress.key` | 今の要素のキー。list なら 0 始まりの番号、map ならキー | `1` |

### iterator で変数名を変える

**iterator**(ループ変数の名前を変える引数)を指定すると、既定の「ブロック名と同じ変数」を別名にできます。`iterator = rule` と書けば、`ingress.value` の代わりに `rule.value` と書きます。ブロック名の `ingress` より「ルール1件」と読める名前のほうが意味が伝わる、というのが主な使い道です。

iterator を付けたあとで `ingress.value` と書くと、plan で次のエラーになります。`ingress.value` が「ingress という型の value という名前のリソース」と解釈されてしまうためです。

```text
Error: Reference to undeclared resource
...
A managed resource "ingress" "value" has not been declared in the root
module.
```

### オブジェクトのリストを回す

実務では、ポート番号だけでなく「ポートと許可元の組」を1件として渡すことが多いです。そのとき for_each には**オブジェクト**(lesson03 で見た、名前付きの値をまとめたもの)のリストを渡します。

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

| 行 | 意味 |
|---|---|
| `for_each = var.ingress_rules` | ルール(オブジェクト)のリストを1件ずつ回す |
| `iterator = rule` | 1件分を指す変数の名前を `rule` にする |
| `from_port = rule.value.port` | `rule.value` が今のオブジェクト1件。その `.port` 属性(80 など) |
| `cidr_blocks = [rule.value.cidr]` | 今のオブジェクトの `.cidr` 属性。`cidr_blocks` はリストを受け取る引数なので `[ ]` で包む |

`rule.value.port` は左から「ループ変数 `rule` → 今の要素 `.value` → その中の `port` 属性」と読みます。`.` は「中の値を取り出す」記号です。`var.ingress_rules` が下の2件なら、生成される ingress は次の2つです。

| 回 | `rule.key` | `rule.value` | 生成される ingress |
|---|---|---|---|
| 1回目 | `0` | `{ port = 80, cidr = "10.0.0.0/16" }` | 80 番を `10.0.0.0/16` から許可 |
| 2回目 | `1` | `{ port = 443, cidr = "0.0.0.0/0" }` | 443 番をどこからでも許可 |

`10.0.0.0/16` は「`10.0.` で始まるアドレス全部」という CIDR で、社内ネットワークなど限られた範囲を表すときによく使います。

AWS プロバイダで plan すると、実際に次の2つが作られる予告になりました(content に `description = "rule-${rule.key}"` も足して、`rule.key` が 0・1 になることも確認しています)。

```text
          + {
              + cidr_blocks      = [
                  + "0.0.0.0/0",
                ]
              + description      = "rule-1"
              + from_port        = 443
              + protocol         = "tcp"
              + to_port          = 443
              ...
            },
          + {
              + cidr_blocks      = [
                  + "10.0.0.0/16",
                ]
              + description      = "rule-0"
              + from_port        = 80
              + protocol         = "tcp"
              + to_port          = 80
              ...
            },
```

🟡 iterator があるコードでは「どの変数がループ 1 周分を指すか」を最初に確認しましょう。

### サンプルの読み方

サンプルは、上の dynamic + iterator が生成するルールを for 式で再現しています。

```hcl
locals {
  ingress_rules = [                                 # オブジェクト2件のリスト
    { port = 80, cidr = "10.0.0.0/16" },
    { port = 443, cidr = "0.0.0.0/0" },
  ]

  lines = [for r in local.ingress_rules : "${r.port} from ${r.cidr}"]
}

output "ingress" {
  value = join(", ", local.lines)                   # ", " でつないで1つの文字列に
}
```

- for 式の `r` が、dynamic の `rule.value` に当たります。dynamic では `rule.value.port`、for 式では `r.port` と書きます
- `"${r.port} from ${r.cidr}"` の `${ }` は lesson04 で見た文字列補間で、`{ }` の中の値を文字列に埋め込みます。数値の 80 も文字列 `"80"` として埋め込まれます

実行結果です。

```text
ingress = "80 from 10.0.0.0/16, 443 from 0.0.0.0/0"
```

## ch03 dynamicの使いどころと使いすぎ問題

### dynamic が向く場面

dynamic が向くのは「ルールの件数が variable や環境によって変わる」場合だけです。たとえば「本番は 443 だけ、検証環境は 22 と 443」のように、環境ごとに渡すリストが変わるケースです。

件数が 0 件になるケースも dynamic なら扱えます。ch01 の例で `allowed_ports` に空のリスト `[]` を渡して plan すると、ingress は1つも生成されず、エラーにもなりませんでした。

```text
      + ingress                = (known after apply)
Plan: 1 to add, 0 to change, 0 to destroy.
```

ingress ブロックが1つも生成されなかったため、ch01 のように具体的なルールが並ばず、`(known after apply)`(apply してみるまで決まらない)と表示されています。

### 固定の少数なら直書き

固定の 2〜3 個なら、ブロックをそのまま並べて書くほうが読みやすく、plan の差分も追いやすくなります。

```hcl
# 固定 2 個なら直書きのほうが読みやすい
ingress {
  from_port = 80     # 1つ目: 80 番
  to_port   = 80
}
ingress {
  from_port = 443    # 2つ目: 443 番
  to_port   = 443
}
```

直書きなら、コードを開いた瞬間に「80 と 443 を許可している」と分かります。dynamic だと、for_each に渡している変数の中身(別ファイルの variable の default や tfvars)を探しに行かないと、何が許可されているか分かりません。ch01 で確かめたとおり、どちらで書いても Terraform が作るものは同じなので、読みやすさで選んでよいのです。

### dynamic の中に dynamic

実務レビューでは「dynamic の中に dynamic」のようなネストは可読性が大きく落ちるため避けられる傾向があり、HashiCorp(Terraform の開発元)のスタイルガイドも dynamic の乱用を戒めています。ネストした dynamic とは、たとえば次のような形です(`rule` や `condition` は形を示すための名前で、特定のリソース型の書き方ではありません)。

```hcl
dynamic "rule" {                       # 外側: rule ブロックを繰り返す
  for_each = var.rules
  content {
    name = rule.value.name
    dynamic "condition" {              # 内側: rule の中の condition ブロックをさらに繰り返す
      for_each = rule.value.conditions # 外側の1件が持つ条件のリスト
      content {
        field = condition.value.field
      }
    }
  }
}
```

| 行 | 意味 |
|---|---|
| `dynamic "rule"` / `for_each = var.rules` | ルールのリストの件数だけ `rule` ブロックを作る |
| `dynamic "condition"` | 各 `rule` ブロックの中に、さらに `condition` ブロックを繰り返し作る |
| `for_each = rule.value.conditions` | 外側の「今のルール1件」が持つ `conditions` リストを回す |
| `condition.value.field` | 内側の「今の条件1件」の `field` 属性 |

読むときは「外側の変数(`rule`)と内側の変数(`condition`)がそれぞれ何の1件を指しているか」を分けて追います。ここまで来ると、生成される結果を頭の中で組み立てるのはかなり大変です。

⚪ 読解時は「この dynamic は可変件数だから必要なのか、単に短く書きたかっただけか」を判断できれば十分です。

### サンプルの読み方

サンプルは「件数が多ければ dynamic を検討する」という判断を、lesson04 の条件式で表したものです。

```hcl
locals {
  rules = ["http", "https", "ssh", "monitoring"]                 # ルール名4件

  decision = length(local.rules) >= 3 ? "dynamic" : "static"     # 3件以上なら "dynamic"
}

output "decision" {
  value = local.decision
}

output "rule_count" {
  value = length(local.rules)                                    # 件数
}
```

- `length(...)` は要素数を返す関数です(lesson05)。ここでは 4
- `条件 ? A : B` は lesson04 の条件式で、条件が true なら A、false なら B になります。`>=` は「以上」の比較です
- 4 は 3 以上なので `decision` は `"dynamic"` になります

```text
decision = "dynamic"
rule_count = 4
```

実際の判断は件数だけでなく「件数が環境で変わるか」で決まります。「3件以上」はこの演習のための目安です。

# Lesson 08 for_each

for_each はコレクションの要素ごとにリソースを作るメタ引数で、現場では count よりも好まれることが多い書き方です。set / map それぞれでの使い方、作られたリソースの参照方法、count との使い分けの流儀を学びます。

## ch01 setでfor_each — each.value

### for_each とは

**for_each**(コレクションの要素ごとにリソースを1つずつ作るメタ引数)は、lesson07 の count と並ぶ「複数リソース作成」の道具です。**メタ引数**(lesson07 で見た、リソースの型によらず使える共通の引数)なので、`terraform_data` にも `aws_s3_bucket` にも同じ書き方で付けられます。

count が「3個作る」のように**個数**を渡すのに対し、for_each には**名前の集まり**を渡します。渡した集まりの要素1つにつき、リソースが1つ作られます。

### set と toset

for_each に渡せるのは **set**(集合。順序がなく、同じ値を2つ持たない値の集まり)か、map(lesson03 で見たキーと値の組。ch02 で扱います)だけです。lesson03 の list(`["sato", "suzuki"]` のような順序付きの並び)はそのまま渡せません。

そこで **`toset`**(リストを set に変換する関数)を使います。toset には次の性質があります。

| 入力 | `toset(...)` の結果 | ポイント |
|---|---|---|
| `["suzuki", "sato"]` | `sato`、`suzuki` の set | 文字列の set は表示がアルファベット順になる |
| `["suzuki", "sato", "sato"]` | `sato`、`suzuki` の set | 重複した `sato` は1つにまとまる |

実際に `toset(["suzuki", "sato", "sato"])` を output で表示すると、こうなります。

```text
s = toset([
  "sato",
  "suzuki",
])
```

試しにリストをそのまま `for_each = var.users` と書くと、plan の段階で次のエラーになります。

```text
Error: Invalid for_each argument
...
    │ var.users is tuple with 2 elements

The given "for_each" argument value is unsuitable: the "for_each" argument
must be a map, or set of strings, and you have provided a value of type
tuple.
```

「for_each には map か文字列の set を渡してください。tuple(型を指定しない `[...]` の値のこと。リストの一種)が渡されました」という意味です。このエラーを見たら `toset(...)` で包み忘れていないかを確認します。

### each.value

for_each を付けたブロックの中では **`each.value`**(今処理している要素の値)が使えます。`each` は for_each 専用の特別な名前で、要素ごとに中身が入れ替わります。set の場合は `each.key` も使えますが、`each.value` と同じ値になります(`sato` の回なら両方 `"sato"`)。

### サンプルを1行ずつ

```hcl
variable "users" {
  default = ["sato", "suzuki"]                   # 名前のリスト(lesson03)
}

resource "terraform_data" "user" {
  for_each = toset(var.users)                    # リストを set にして、要素ごとに1つ作る
  input    = format("user-%s", each.value)       # %s に今の要素が入る → "user-sato" など
}

output "sato" {
  value = terraform_data.user["sato"].output     # キー "sato" のリソースの output 属性
}

output "user_keys" {
  value = join(",", keys(terraform_data.user))   # 作られたリソースのキー一覧を "," でつなぐ
}
```

- `format("user-%s", each.value)` は lesson05 で見た関数です。`%s` の位置に文字列が入ります
- `terraform_data.user["sato"]` の `[ ]` は「キーで1つを取り出す」記号です。for_each で作ったリソースは、**要素の値をキーとするマップ**になります
- `keys(...)`(lesson05)はマップのキーをアルファベット順のリストで返し、`join(",", ...)` はそれを `,` でつないだ1つの文字列にします

plan を見ると、1つの resource ブロックから2つのリソースが作られることが分かります。

```text
  # terraform_data.user["sato"] will be created
  + resource "terraform_data" "user" {
      + id     = (known after apply)
      + input  = "user-sato"
      + output = (known after apply)
    }

  # terraform_data.user["suzuki"] will be created
  + resource "terraform_data" "user" {
      + id     = (known after apply)
      + input  = "user-suzuki"
      + output = (known after apply)
    }

Plan: 2 to add, 0 to change, 0 to destroy.
```

`# terraform_data.user["sato"]` の部分が**リソースアドレス**(state の中でリソースを区別する名前)です。count なら `terraform_data.user[0]` のように番号が付きましたが、for_each では `["sato"]` のように要素の値が付きます。番号ではなく名前で管理されるので、lesson07 ch03 で見た「真ん中を消すと後ろの index が全部ずれる」問題が起きません(ch04 で実際に比べます)。

apply 後の output は次のとおりです。

```text
sato = "user-sato"
user_keys = "sato,suzuki"
```

### 実務での読み方

🔴 実務では IAM ユーザーや S3 バケットなど「名前の集まりから同種のリソースを並べる」場面の標準形です。`for_each = toset(...)` を見たら要素ごとの複製と読んでください。

```hcl
resource "aws_iam_user" "member" {
  for_each = toset(var.user_names)   # 読解例: 名前ごとにユーザーを作成
  name     = each.value
}
```

| 行 | 意味 |
|---|---|
| `resource "aws_iam_user" "member"` | **IAM ユーザー**(AWS にログインや操作をするためのアカウント。IAM は AWS の権限管理サービス)を定義 |
| `for_each = toset(var.user_names)` | `var.user_names`(例: `["ito", "kato"]`)を set にして、名前1つにつきユーザーを1人作る |
| `name = each.value` | AWS 上のユーザー名を、今の要素(`"ito"` など)にする |

`var.user_names` が `["ito", "kato"]` なら、`aws_iam_user.member["ito"]` と `aws_iam_user.member["kato"]` の2人が作られます。

## ch02 mapでfor_each — each.keyとeach.value

### map を for_each に渡す

for_each には set のほかに **map**(lesson03 で見たキーと値の組)もそのまま渡せます。toset は要りません。map を渡すと、ブロックの中で次の2つが使えます。

| 書き方 | 中身 | 下のサンプルの `web` の回 |
|---|---|---|
| `each.key` | 今の要素の**キー**(`=` の左側) | `"web"` |
| `each.value` | 今の要素の**値**(`=` の右側) | `"t3.small"` |

set のときは `each.key` と `each.value` が同じ値でしたが、map では別々の値になります。「名前 → 設定値」というマップから、名前と設定を同時に使ってリソースを組み立てられるため、set よりも表現力が高い形です。作られたリソースのキーは、map のキー(`api`、`web`)になります。

### サンプルを1行ずつ

```hcl
variable "instances" {
  default = {
    api = "t3.medium"                    # キー api → 値 "t3.medium"
    web = "t3.small"                     # キー web → 値 "t3.small"
  }
}

resource "terraform_data" "instance" {
  for_each = var.instances               # map はそのまま渡せる。要素は2つなので2つ作る
  input    = format("%s runs on %s", each.key, each.value)
                                         # 1つ目の %s にキー、2つ目の %s に値が入る
}

output "web" {
  value = terraform_data.instance["web"].output       # キー "web" のリソースの output 属性
}

output "instance_keys" {
  value = join(",", keys(terraform_data.instance))    # キー一覧を "," でつなぐ
}
```

- `{ ... }` の中に `キー = 値` を1行ずつ書くのが map の書き方です
- `format` は `%s` が複数あると、後ろの引数を前から順に埋めます。`format("%s runs on %s", "web", "t3.small")` は `"web runs on t3.small"` になります

plan では、map のキーがそのままリソースアドレスの `[" "]` の中に入ります。

```text
  # terraform_data.instance["api"] will be created
  + resource "terraform_data" "instance" {
      + id     = (known after apply)
      + input  = "api runs on t3.medium"
      + output = (known after apply)
    }

  # terraform_data.instance["web"] will be created
  + resource "terraform_data" "instance" {
      + id     = (known after apply)
      + input  = "web runs on t3.small"
      + output = (known after apply)
    }

Plan: 2 to add, 0 to change, 0 to destroy.
```

apply 後の output です(output 名のアルファベット順)。

```text
instance_keys = "api,web"
web = "web runs on t3.small"
```

### 実務での読み方

実務では `{ web = "t3.small", api = "t3.medium" }` のような「インスタンス名 → タイプ」のマップから EC2 を並べる形が典型で、variable にマップを持たせて for_each で回すのは現場コードの最頻出パターンの1つです。

```hcl
resource "aws_instance" "app" {
  for_each      = var.instances          # 読解例: 名前→タイプのマップ
  instance_type = each.value             # 値(タイプ)
  tags          = { Name = each.key }    # キー(名前)
}
```

| 行 | 意味 |
|---|---|
| `resource "aws_instance" "app"` | **EC2 インスタンス**(AWS で借りる仮想サーバー1台)を定義 |
| `for_each = var.instances` | `{ api = "t3.medium", web = "t3.small" }` の要素ごとにサーバーを1台作る |
| `instance_type = each.value` | **インスタンスタイプ**(サーバーの性能の種類。`t3.small` は小さめ、`t3.medium` はその1段上)に値を使う |
| `tags = { Name = each.key }` | **タグ**(リソースに付ける名札。`Name` タグは AWS の管理画面に名前として表示される)にキーを使う |

この例では `aws_instance.app["api"]`(t3.medium、Name タグ `api`)と `aws_instance.app["web"]`(t3.small、Name タグ `web`)の2台ができます。サーバーを1台足したいときは、map に `batch = "t3.large"` のように1行足すだけです。

🔴 each.key / each.value がそれぞれ何を指すかを即答できるようにしましょう。

## ch03 for_eachリソースの参照 — [キー]とvalues()

### for_each で作ったリソースは「マップ」

lesson07 の count で作ったリソースは**リスト**だったので、`リソース[0]` の番号(index)で1つを取り出し、`リソース[*].属性` の splat(lesson06)で全部の属性をまとめて取れました。

for_each で作ったリソースは**マップ**(キー → リソース1つ分)です。そのため参照の形が変わります。

| やりたいこと | count(リスト) | for_each(マップ) |
|---|---|---|
| 1つを取り出す | `terraform_data.q[0]` | `terraform_data.q["mail"]` |
| 全部の属性をリストにする | `terraform_data.q[*].output` | `values(terraform_data.q)[*].output` |
| 個数 | `length(terraform_data.q)` | `length(terraform_data.q)`(同じ) |

for_each のリソースに `[0]` と書くと、plan で次のエラーになります。

```text
Error: Invalid index
...
    │ terraform_data.q is object with 2 attributes

The given key does not identify an element in this collection value. An
object only supports looking up attributes by name, not by numeric index.
```

「名前(キー)でしか取り出せず、番号では取り出せません」という意味です。

### values() + splat で全要素を取り出す

**`values`**(lesson05 で見た、マップの値だけを並べたリストを返す関数)を使うと、マップをリストに変えられます。並び順は**キーのアルファベット順**です。リストになれば splat `[*]` が使えます。

`values(terraform_data.queue)[*].output` を左から順に読むと次のとおりです。

| 部分 | 結果 |
|---|---|
| `terraform_data.queue` | `{ mail = (mail のリソース), sync = (sync のリソース) }` というマップ |
| `values(...)` | `[(mail のリソース), (sync のリソース)]` というリスト(キー順) |
| `[*].output` | `["queue-mail", "queue-sync"]`(各リソースの output 属性だけを集めたリスト) |

### サンプルを1行ずつ

```hcl
variable "queues" {
  default = ["mail", "sync"]
}

resource "terraform_data" "queue" {
  for_each = toset(var.queues)                    # mail と sync の2つを作る
  input    = format("queue-%s", each.value)       # "queue-mail" / "queue-sync"
}

output "mail" {
  value = terraform_data.queue["mail"].output     # キー "mail" の1つだけ
}

output "all" {
  value = join(",", values(terraform_data.queue)[*].output)  # 全部の output を "," でつなぐ
}

output "queue_count" {
  value = length(terraform_data.queue)            # 作られたリソースの数
}
```

実行結果です。`queue_count` は数値なので `"..."` が付きません。

```text
all = "queue-mail,queue-sync"
mail = "queue-mail"
queue_count = 2
```

### for 式で書く形

実務では、values と splat の代わりに lesson06 の for 式で書くこともあります。for_each のリソースに for 式を使うと、`k` にキー、`r` にリソース1つ分が入ります。

```hcl
output "by_key" {
  value = { for k, r in terraform_data.queue : k => r.output }  # キー → output のマップを作る
}
```

`=>` は「左をキー、右を値にする」という for 式の記号です(lesson06)。表示は次のようになります。

```text
by_key = {
  "mail" = "queue-mail"
  "sync" = "queue-sync"
}
```

### 実務での読み方

実務コードで `values(aws_subnet.private)[*].id` といった参照を見たら「for_each で作った全サブネットの ID をリスト化している」と読めます。**サブネット**は、AWS のネットワーク(VPC)をさらに小さく区切った区画のことで、サーバーはどれかのサブネットに置きます。

```hcl
locals {
  subnet_ids = values(aws_subnet.private)[*].id   # 読解例: 全要素の id
  main_id    = aws_subnet.private["main"].id      # キーで個別参照
}
```

| 行 | 意味 |
|---|---|
| `subnet_ids = values(aws_subnet.private)[*].id` | for_each で作った `aws_subnet.private` の全サブネットの `id`(AWS が付ける識別子)をキー順のリストにする |
| `main_id = aws_subnet.private["main"].id` | キー `"main"` のサブネット1つだけの `id` を取る |

🟡 「for_each 化されたリソース = マップ」という頭の切り替えが、このレッスンの読解ポイントです。

## ch04 countとfor_eachの使い分け — 現場の流儀

### 位置で管理するか、キーで管理するか

count と for_each はどちらも複数リソースを作りますが、現場では**キーの安定性**(要素が増えたり減ったりしても、残った要素の名前が変わらないこと)から for_each が好まれることが多いです。

- count は「リストの何番目か」(index)でリソースを管理します。そのため要素の増減で index がずれます(lesson07 ch03 参照)
- for_each は「キー」でリソースを管理します。途中の要素を消しても、他のリソースのキーは変わりません

### 同じものを2通りに書く

```hcl
# count 版(位置で管理)         # for_each 版(キーで管理・増減に強い)
count = length(var.envs)        for_each = toset(var.envs)
input = var.envs[count.index]   input    = each.value
```

| count 版 | for_each 版 | 意味 |
|---|---|---|
| `count = length(var.envs)` | `for_each = toset(var.envs)` | 要素の数だけ作る / 要素ごとに作る |
| `var.envs[count.index]` | `each.value` | 今の要素の値 |
| アドレスは `by_count[0]` `[1]` `[2]` | アドレスは `by_each["dev"]` `["prod"]` `["stg"]` | state に記録される名前 |
| 全部の属性は `by_count[*].output` | 全部の属性は `values(by_each)[*].output` | 参照の形(ch03) |

サンプルの output は次のとおりで、作られる中身は同じです。

```text
count_style = "dev,prod,stg"
each_keys = "dev,prod,stg"
```

### 真ん中の要素を消すと何が起きるか

サンプルを apply したあと、`envs` の default を `["dev", "prod", "stg"]` から `["dev", "stg"]` に変えて(`prod` を消して)plan すると、実際に次の予告が出ます。

```text
  # terraform_data.by_count[1] will be updated in-place
  ~ resource "terraform_data" "by_count" {
        id     = "..."
      ~ input  = "prod" -> "stg"
      ~ output = "prod" -> (known after apply)
    }

  # terraform_data.by_count[2] will be destroyed
  # (because index [2] is out of range for count)
  - resource "terraform_data" "by_count" {
      - id     = "..." -> null
      - input  = "stg" -> null
      - output = "stg" -> null
    }

  # terraform_data.by_each["prod"] will be destroyed
  # (because key ["prod"] is not in for_each map)
  - resource "terraform_data" "by_each" {
      - id     = "..." -> null
      - input  = "prod" -> null
      - output = "prod" -> null
    }

Plan: 0 to add, 1 to change, 2 to destroy.
```

| 版 | 起きること | 理由 |
|---|---|---|
| count 版 | `[1]` の中身が `prod` → `stg` に書き換わり、`[2]`(元の stg)が削除される | stg が index 2 から 1 に繰り上がったため。`out of range for count` は「count の範囲外になった」の意味 |
| for_each 版 | `["prod"]` だけが削除される。`["dev"]` `["stg"]` は何も変わらない | キーで管理しているので、残った要素の名前は変わらない |

消したかったのは prod だけなのに、count 版では無関係な stg まで巻き込まれています。`-> null` は「値がなくなる(削除される)」という意味です。

なお `terraform_data` は input の変更をその場で書き換える(`~ update in-place`)ので、ここでは「書き換え」で済んでいます。本物のリソースでは、名前を変えると作り直しになる型が多くあります(例: S3 バケットの名前)。その場合 count 版の `[1]` は `-/+`(いったん削除して作り直し)になり、中に入っていたデータごと消える事故につながります。

### 使い分けの目安

使い分けの目安は「まったく同質な複製やオンオフ(`? 1 : 0`)は count、名前で区別できる集まりは for_each」です。

| 場面 | 向いているもの | 例 |
|---|---|---|
| 作るか作らないかの切り替え | count | `count = var.enable_log ? 1 : 0`(lesson07 ch02) |
| 名前の付いた集まり | for_each | 環境名、ユーザー名、バケット名の一覧 |
| 名前ごとに設定が違う | for_each(map) | `{ api = "t3.medium", web = "t3.small" }`(ch02) |

ただしこれは流儀であり、既存コードベースの慣習に合わせるのが実務の基本です。また、すでに count で作ったリソースを for_each に書き換えると、アドレスが `[0]` から `["dev"]` に変わるため、何もしないと plan は「全部削除して全部作り直し」になります。`["dev", "prod"]` を count で apply したあと for_each に書き換えて plan すると、実際にこうなります。

```text
  # terraform_data.env[0] will be destroyed
  # (because resource does not use count)
  # terraform_data.env[1] will be destroyed
  # (because resource does not use count)
  # terraform_data.env["dev"] will be created
  # terraform_data.env["prod"] will be created
Plan: 2 to add, 0 to change, 2 to destroy.
```

実務で書き換えるときは、state 上の名前を付け替える **`moved` ブロック**(「旧アドレスのリソースは新アドレスに引っ越した」と Terraform に伝えるブロック)を一緒に書きます。

```hcl
moved {
  from = terraform_data.env[0]       # 引っ越し元(count 時代のアドレス)
  to   = terraform_data.env["dev"]   # 引っ越し先(for_each のアドレス)
}
```

`[1]` → `["prod"]` の moved も足して plan すると、`has moved to` と表示され `Plan: 0 to add, 0 to change, 0 to destroy.`(何も作り直さない)になります。state の扱いは lesson12 で詳しく見ます。

🟡 コードレビューで「count を for_each にしませんか」という指摘は定番なので、理由を説明できるようにしましょう。

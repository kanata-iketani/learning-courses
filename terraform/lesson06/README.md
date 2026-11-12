# Lesson 06 for式とsplat

for式と splat([*])は、リストやマップを別の形に変換するための HCL の中心的な道具です。実務コードでは変数からリソース定義用のデータ構造を組み立てる場面で必ず登場します。読んで意味が取れるようになりましょう。

## ch01 リストのfor式 — [for x in ...]

### for式とは

**for式**(リストやマップの各要素を変換して、新しいリストやマップを作る式)は、Python のリスト内包表記 `[x.upper() for x in names]` に当たる書き方です。Terraform にはふつうのプログラミング言語のような `for` 文(処理をくり返す命令)がありません。代わりに「元の集まりから新しい集まりを作る**式**」として for式を使います。

このチャプターでは、リストを作る for式を見ます。形は次のとおりです。

```hcl
[for x in var.list : 式]
```

| 部品 | 意味 |
|---|---|
| `[` `]` | 外側の角かっこ。「結果はリストになる」という印 |
| `for x in var.list` | `var.list` の要素を先頭から1つずつ取り出し、そのたびに `x` という名前で呼ぶ |
| `:` | 区切り。ここから右が「1要素ごとに作る値」 |
| `式` | `x` を使って新しい要素を作る式。全要素に同じ変換がかかる |

`x` の部分は自分で好きな名前を付けられます(`n`、`u`、`name` など)。この名前は for式の中でだけ使えます。元のリスト `var.list` は書き換わらず、変換後の**新しいリスト**ができます。

### 小さな具体例

`var.names` が `["ayame", "botan", "kaede"]` のとき、`[for n in var.names : upper(n)]` は次のように計算されます(`upper` は lesson05 で見た「大文字にする」関数です)。

| 取り出した n | upper(n) |
|---|---|
| `"ayame"` | `"AYAME"` |
| `"botan"` | `"BOTAN"` |
| `"kaede"` | `"KAEDE"` |

結果は `["AYAME", "BOTAN", "KAEDE"]` です。順序は元のリストと同じです。

### index も使う形 `for i, x in ...`

`for` のあとに名前を2つ書くと、1つ目に **index**(要素の位置番号。0 始まり)、2つ目に要素が入ります。

```hcl
locals {
  upper_names = [for n in var.names : upper(n)]           # 全要素を大文字に
  hosts       = [for i, n in var.names : "${i}-${n}"]     # index 付き
}
```

- 1行目: `n` に要素が入り、`upper(n)` が新しい要素になります
- 2行目: `i` に 0, 1, 2、`n` に要素が入ります。`"${i}-${n}"` は lesson04 で見た**文字列補間**(`${ }` の中の値を文字列に埋め込む書き方)なので、結果は `["0-ayame", "1-botan", "2-kaede"]` です

### サンプルを1行ずつ

```hcl
variable "names" {
  default = ["ayame", "botan", "kaede"]          # 元のリスト
}

locals {
  upper_names = [for n in var.names : upper(n)]  # 各要素を大文字にした新しいリスト
  hosts = [for i, n in var.names : format("%02d-%s", i + 1, n)]
}

output "upper_joined" {
  value = join(",", local.upper_names)           # リストを , でつないで1本の文字列に
}

output "hosts" {
  value = join(",", local.hosts)
}
```

`hosts` の行を分解します。

| 部分 | 意味 |
|---|---|
| `for i, n in var.names` | `i` に 0, 1, 2、`n` に `"ayame"` などが入る |
| `i + 1` | 0 始まりを 1 始まりにする(1, 2, 3) |
| `format("%02d-%s", ...)` | lesson05 で見た `format`。`%02d` は「整数を2桁で、足りなければ前を 0 で埋める」、`%s` は「文字列をそのまま入れる」 |

`format("%02d-%s", 1, "ayame")` は `"01-ayame"` になります。`join` も lesson05 で見た関数で、リストを区切り文字でつないだ文字列を返します。実行結果は次のとおりです。

```text
hosts = "01-ayame,02-botan,03-kaede"
upper_joined = "AYAME,BOTAN,KAEDE"
```

実務では「ユーザー名のリストからメールアドレスのリストを作る」「名前のリストからリソース定義用の値を組み立てる」という前処理として必ず登場します。

### リストをそのまま output したときの見た目

🔴 なお、リストをそのまま output すると複数行の形式で表示されます。この見た目にも慣れておきましょう。`local.upper_names` を join せずに output すると、こう出ます。

```text
upper_names = [
  "AYAME",
  "BOTAN",
  "KAEDE",
]
```

1要素1行で、最後の要素にもカンマが付きます。さらに `tolist(...)`(値を list 型に変換する関数)で包んでから output すると、表示が `tolist([ ... ])` になります。

```text
upper_names = tolist([
  "AYAME",
  "BOTAN",
  "KAEDE",
])
```

中身は同じです。違いは型の扱いで、for式がそのまま作るのは **tuple**(要素ごとに型が違ってもよい並び)、`tolist` を通すと **list**(全要素が同じ型の並び)になります。Terraform は list 型の値を表示するとき `tolist(...)` と書き添えます。実務の plan 出力でも `tolist([...])` はよく出るので、「中身はふつうのリスト」と読めれば十分です。

## ch02 mapを作るfor式 — {for k, v in ...}

### マップを作る for式の形

ch01 では `[ ]` でリストを作りました。外側を `{ }` にすると、for式は**マップ**(lesson03 で見た「キーと値の組」の集まり)を作ります。

```hcl
{for k, v in var.map : k => 変換式}
```

| 部品 | 意味 |
|---|---|
| `{` `}` | 外側の波かっこ。「結果はマップになる」という印 |
| `for k, v in var.map` | マップの組を1つずつ取り出し、`k` にキー、`v` に値を入れる |
| `:` | 区切り。ここから右が「1組ごとに作るもの」 |
| `k => 変換式` | `=>` の左が新しいマップの**キー**、右が新しい**値** |

`=>` は「このキーにこの値を対応させる」という矢印で、マップを作る for式の中でだけ使います。ふつうのマップを書くときの `api = "t3.medium"` の `=` に当たります。

マップを for で回すと、キーの**アルファベット順**に取り出されます(lesson05 で見た `keys` / `values` と同じ順です)。

### 小さな具体例

`var.sizes` が `{ api = "t3.medium", web = "t3.small" }` のとき(`t3.medium` などは AWS のサーバーの大きさを表す名前ですが、ここではただの文字列です)、`{ for k, v in var.sizes : k => upper(v) }` は次のように計算されます。

| k | v | 新しいキー k | 新しい値 upper(v) |
|---|---|---|---|
| `"api"` | `"t3.medium"` | `"api"` | `"T3.MEDIUM"` |
| `"web"` | `"t3.small"` | `"web"` | `"T3.SMALL"` |

結果は `{ api = "T3.MEDIUM", web = "T3.SMALL" }` です。キーはそのままで、値だけを作り替えています。この「キーを保ったまま値だけ変える」形が最もよく見る使い方です。

### リストからマップを作る

元がリストでも `{ }` と `=>` を使えばマップを作れます。このときは `for x in var.list` と名前を1つだけ書き、キーも値も自分で組み立てます。

```hcl
locals {
  # 値だけを変換した新しいマップ
  upper_sizes = { for k, v in var.sizes : k => upper(v) }
  # リスト → マップ(キー => 値 を自分で組み立てる)
  name_len = { for n in var.names : n => length(n) }
}
```

`var.names` が `["sato", "suzuki"]` なら、`name_len` は `{ sato = 4, suzuki = 6 }` になります(`length` は文字列に使うと文字数を返します)。リストからマップを作る形は、後の lesson08 で学ぶ for_each(マップのキーごとにリソースを作る仕組み)の前処理として実務で多用されます。

🔴 「`[...]` ならリストを作る for式、`{...}` と `=>` ならマップを作る for式」という見分け方を身につけると、実務コードの読解速度が大きく変わります。

### サンプルを1行ずつ

```hcl
locals {
  labels = { for k, v in var.sizes : k => "${k} runs on ${v}" }
  name_len = { for n in var.names : n => length(n) }
}

output "web_label" {
  value = local.labels["web"]               # マップから "web" キーの値を取り出す
}

output "sato_len" {
  value = local.name_len["sato"]            # "sato" キーの値(文字数)
}

output "label_keys" {
  value = join(",", keys(local.labels))     # キーの一覧を , でつなぐ
}
```

- `labels`: キーはそのまま、値を `"${k} runs on ${v}"` という文字列にします。`"web"` の値は `"web runs on t3.small"` です
- `local.labels["web"]`: lesson03 で見たマップの参照 `マップ["キー"]` です
- `keys(...)`: マップのキー一覧をアルファベット順のリストで返します(lesson05)

実行結果です。

```text
label_keys = "api,web"
sato_len = 4
web_label = "web runs on t3.small"
```

`labels` を join せずにそのまま output すると、マップは次の形で表示されます。

```text
labels = {
  "api" = "api runs on t3.medium"
  "web" = "web runs on t3.small"
}
```

### キーが重なるとエラーになる

リストからマップを作るとき、`=>` の左が同じ値になる要素が2つあると、マップのキーが重なります。マップのキーは1つしか持てないので、Terraform はエラー `Duplicate object key`(キーの重複)で止まります。

```text
Error: Duplicate object key

Two different items produced the key "dev" in this 'for' expression. If
duplicates are expected, use the ellipsis (...) after the value expression to
enable grouping by key.
```

メッセージにあるとおり、値の後ろに `...` を付けて `u.team => u.name...` と書くと、同じキーの値をリストにまとめる**グループ化**になります。たとえばチーム名をキーにすると `{ dev = ["sato", "kato"], ops = ["ito"] }` のような結果になります。実務コードで `=>` の右の末尾に `...` があったら「キーごとにまとめている」と読んでください。

## ch03 ifでフィルタするfor式

### if でフィルタする形

for式の末尾に `if 条件` を付けると、条件を満たす要素だけを残せます(条件に合わない要素を捨てることを**フィルタ**と呼びます)。Python の `[x for x in hosts if x.endswith("-prod")]` と同じ考え方です。

```hcl
[for x in var.list : 式 if 条件]
```

| 部品 | 意味 |
|---|---|
| `for x in var.list` | 要素を1つずつ `x` として取り出す(ch01 と同じ) |
| `: 式` | 残った要素から作る新しい値 |
| `if 条件` | `条件` が true の要素だけを結果に入れる。false の要素は捨てる |

`if` は必ず一番後ろに置きます。Terraform は「条件で絞る → 残った要素に `: 式` をかける」の順に考えると読みやすくなります。変換とフィルタを1つの for式で同時に行えるわけです。

条件の部分には true / false になる式を書きます。lesson04 で見た比較演算子(`==` 等しい、`!=` 等しくない など)や、true / false を返す関数を使います。

### endswith と startswith

この形とよく一緒に使われるのが次の2つの関数です。

| 関数 | 意味 | 例 |
|---|---|---|
| `endswith(文字列, 接尾辞)` | 文字列が指定の文字で**終わる**なら true | `endswith("web-prod", "-prod")` → `true` |
| `startswith(文字列, 接頭辞)` | 文字列が指定の文字で**始まる**なら true | `startswith("web-prod", "db-")` → `false` |

**接尾辞**は文字列の末尾の部分、**接頭辞**は先頭の部分のことです。実務ではリソースの名前に `-prod`(本番)や `-dev`(開発)を付けて区別することが多く、「本番用のリソースだけ」「特定のサフィックスを持つバケットだけ」を抜き出す前処理として頻出です(**バケット**は lesson01 で見た S3 のファイル入れのことです)。

```hcl
locals {
  prod_only = [for b in var.buckets : b if endswith(b, "-prod")]
}
```

`: b` は「取り出した要素をそのまま使う(変換しない)」という意味です。フィルタだけしたいときはこの形になります。

### 小さな具体例

サンプルの `var.hosts` は `["web-prod", "web-dev", "db-prod", "cache-dev"]` です。`[for h in var.hosts : h if endswith(h, "-prod")]` は次のように計算されます。

| h | endswith(h, "-prod") | 結果に入るか |
|---|---|---|
| `"web-prod"` | true | 入る |
| `"web-dev"` | false | 入らない |
| `"db-prod"` | true | 入る |
| `"cache-dev"` | false | 入らない |

結果は `["web-prod", "db-prod"]` です。残った要素の順序は元のリストの順のままです。

### サンプルを1行ずつ

```hcl
locals {
  prod_hosts = [for h in var.hosts : h if endswith(h, "-prod")]           # -prod だけ残す
  dev_upper  = [for h in var.hosts : upper(h) if endswith(h, "-dev")]     # -dev だけ残して大文字に
}

output "prod_hosts" {
  value = join(",", local.prod_hosts)   # "web-prod,db-prod"
}

output "prod_count" {
  value = length(local.prod_hosts)      # 残った要素数 2
}

output "dev_upper" {
  value = join(",", local.dev_upper)     # "WEB-DEV,CACHE-DEV"
}
```

`dev_upper` は、`-dev` で終わる `"web-dev"` と `"cache-dev"` だけを残し、それぞれに `upper` をかけています。実行結果です。

```text
dev_upper = "WEB-DEV,CACHE-DEV"
prod_count = 2
prod_hosts = "web-prod,db-prod"
```

### マップを作る for式にも付けられる

ch02 のマップ版にも同じように `if` を付けられます。

```hcl
prod_sizes = { for k, v in var.sizes : k => v if k != "web" }   # キーが web 以外の組だけ残す
```

`!=` は「等しくない」なので、キーが `"web"` の組を捨てたマップができます。

🔴 for式に if が付いていたら「絞り込んでから使う」意図だと読めるようにしましょう。

## ch04 splat[*]とflatten — ネストの平坦化

### splat `[*]` とは

**splat**(`[*]` で、オブジェクトのリストから特定の属性だけをまとめて取り出す記法)は `var.servers[*].name` のように書き、`[for s in var.servers : s.name]` の省略形です。

前提として、サンプルの `var.servers` は「**オブジェクト**(lesson03 で見た、名前付きの項目を持つ値)のリスト」です。

```hcl
variable "servers" {
  type = list(object({        # 型: 「name と ips を持つオブジェクト」のリスト
    name = string             #   name は文字列
    ips  = list(string)       #   ips は文字列のリスト(IP アドレスの一覧)
  }))
  default = [
    { name = "web", ips = ["10.0.0.1", "10.0.0.2"] },   # 1台目のサーバー
    { name = "db", ips = ["10.0.1.1"] },                 # 2台目のサーバー
  ]
}
```

(**IP アドレス**はネットワーク上の機器の住所を表す番号で、`10.0.0.1` のように書きます)

ここで `var.servers[*].name` は次のように読みます。

| 部分 | 意味 |
|---|---|
| `var.servers` | オブジェクトのリスト |
| `[*]` | 「全要素について」 |
| `.name` | それぞれの `name` 属性を取る |

結果は `["web", "db"]` です。`var.servers[0].name`(0番目の name だけ)の `0` を `*` に変えて「全部」にした、と覚えると読みやすくなります。

### splat するとリストのリストになる場合

`ips` のようにもともとリストである属性を splat すると、結果は「リストのリスト」になります。実際に `var.servers[*].ips` を output すると、こう表示されます。

```text
splat_ips = [
  [
    "10.0.0.1",
    "10.0.0.2",
  ],
  [
    "10.0.1.1",
  ],
]
```

外側のリストの中に、サーバーごとのリストが2つ入っています。このように入れ子になった状態を**ネスト**と呼びます。

### flatten で1段にする

**flatten**(ネストしたリストを1段のリストに平坦化する関数)を使うと、入れ子を外して1本のリストにできます。`flatten(var.servers[*].ips)` の結果はこうです。

```text
all_ips = [
  "10.0.0.1",
  "10.0.0.2",
  "10.0.1.1",
]
```

| 式 | 結果 |
|---|---|
| `var.servers[*].ips` | `[["10.0.0.1", "10.0.0.2"], ["10.0.1.1"]]`(2段) |
| `flatten(var.servers[*].ips)` | `["10.0.0.1", "10.0.0.2", "10.0.1.1"]`(1段) |

`join` や `length` は1段のリストを前提にしているので、リストのリストのままだと思った結果になりません。`length` なら 3 ではなく 2(サーバーの台数)が返ります。

実務では「全 **VPC**(AWS 上に作る自分専用のネットワーク)の**サブネット**(VPC をさらに区切った小さなネットワーク)の ID を1本のリストにまとめる」ような場面で、`flatten(var.vpcs[*].subnets)` の形をよく見ます。

```hcl
locals {
  names   = var.servers[*].name            # 属性だけをまとめて取り出す
  all_ips = flatten(var.servers[*].ips)    # リストのリストを平坦化
}
```

### サンプルを1行ずつ

```hcl
output "names" {
  value = join(",", var.servers[*].name)                # ["web", "db"] を , でつなぐ
}

output "all_ips" {
  value = join(",", flatten(var.servers[*].ips))        # 平坦化してからつなぐ
}

output "ip_count" {
  value = length(flatten(var.servers[*].ips))           # 平坦化したリストの要素数
}
```

関数が入れ子になっているときは、内側から読みます。`all_ips` なら「splat で ips を集める → flatten で1段にする → join でつなぐ」の順です。実行結果です。

```text
all_ips = "10.0.0.1,10.0.0.2,10.0.1.1"
ip_count = 3
names = "web,db"
```

### 練習問題の値について

演習に出てくる `"10.0.1.0/24"` のような値は **CIDR**(サイダー。IP アドレスの範囲を「先頭アドレス/固定するビット数」で表す書き方)です。`/24` は「先頭 24 ビットが共通の範囲」で、`10.0.1.0` 〜 `10.0.1.255` の 256 個を表します。この章ではただの文字列として扱えば十分です(CIDR は lesson10 のモジュールの例でも出てきます)。

🟡 splat はリソース参照でも多用されます(次の lesson07 で `terraform_data.web[*].output` の形が出てきます)。`[*]` を見たら「全要素の属性をまとめて取る」と読んでください。

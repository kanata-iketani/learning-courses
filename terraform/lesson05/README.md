# Lesson 05 関数

HCL には値を加工するための組み込み関数が多数用意されています。このレッスンでは文字列・コレクション・マップ操作の定番関数を演習し、実務コードに頻出する「名前の組み立て」や「タグの merge」を読める状態を目指します。

## ch01 文字列関数（format・join・split ほか）

### 組み込み関数とは

**組み込み関数**(Terraform に最初から用意されている、値を加工するための関数)は `関数名(引数1, 引数2, ...)` の形で呼び出します。Python の関数呼び出しと同じ形です。Terraform では自分で関数を定義することはできず、用意された関数だけを使います。

- `( )` の中に、関数に渡す値(**引数**)を `,` 区切りで並べます
- 関数は値を1つ返すので、locals や output の右辺など、式を書ける場所ならどこでも使えます
- 関数の中に関数を書けます。`upper(replace(x, "-", "_"))` は内側の `replace` が先に計算され、その結果が `upper` に渡されます

このチャプターでは文字列を扱う5つ(+ `lower` / `upper`)を押さえます。以下の結果は `terraform console`(式を入力すると値を表示する対話モード)で実際に確かめたものです。

### format: 型紙に値を流し込む

`format("型紙", 値1, 値2, ...)` は、型紙の中の `%s` などの印を、後ろの値で順番に置き換えます(printf 風の文字列組み立て)。

| 式 | 結果 | 説明 |
|---|---|---|
| `format("%s-%s", "myapp", "prod")` | `"myapp-prod"` | `%s` は文字列を入れる印。1つ目に `myapp`、2つ目に `prod` |
| `format("%d台", 3)` | `"3台"` | `%d` は整数を入れる印 |
| `format("%s-%03d", "web", 7)` | `"web-007"` | `%03d` は「3桁、足りなければ 0 で埋める」 |

印の数より値が少ないと `not enough arguments for "%s"`(`%s` に入れる値が足りない)というエラーになります。lesson04 の補間 `"${var.project}-${var.env}"` と `format("%s-%s", var.project, var.env)` は同じ結果になります。どちらで書かれていても読めるようにしましょう。

### lower / upper: 大文字・小文字をそろえる

`lower("Prod")` は `"prod"`(すべて小文字に)、`upper("my-app")` は `"MY-APP"`(すべて大文字に)です。S3 バケット名のように大文字が使えない名前もあるので、入力が `"Prod"` でも `"PROD"` でも `lower` で小文字にそろえてから組み立てるのが定番です。

### join と split: リストと文字列を行き来する

**リスト**(lesson03 で見た、順番付きの値の並び `[ ]`)と文字列を変換します。

| 式 | 結果 |
|---|---|
| `join("-", ["myapp", "prod", "web"])` | `"myapp-prod-web"` |
| `join(",", [80, 443])` | `"80,443"`(数値は文字列に変換される) |
| `split("-", "myapp-prod-web")` | `["myapp", "prod", "web"]` |
| `split("-", "myapp-prod-web")[1]` | `"prod"` |

- `join(区切り文字, リスト)`: リストの要素を区切り文字でつないで1つの文字列にします。**第1引数が区切り文字**です
- `split(区切り文字, 文字列)`: 文字列を区切り文字で切ってリストにします。`join` の逆です
- `[1]` は関数の結果のリストから、0 始まりで2番目の要素を取り出しています(lesson03 の `var.ports[0]` と同じ書き方)

`split` の結果を output にそのまま出すと、次のように `tolist([...])` と表示されます。`tolist` は「これはリスト型です」という表示上の印で、中身は普通のリストです。

```text
parts = tolist([
  "myapp",
  "prod",
])
```

### replace: 置き換え

`replace(文字列, 探す文字, 置き換える文字)` は、見つかった所を**すべて**置き換えます。`replace("myapp-prod", "-", "_")` は `"myapp_prod"`、`replace("a-b-c", "-", "")` は `"abc"`(空文字に置き換えると削除になる)です。

### サンプルを1行ずつ

```hcl
variable "project" {
  default = "myapp"
}

variable "env" {
  default = "Prod"                                     # わざと大文字まじり
}

locals {
  name  = format("%s-%s", var.project, lower(var.env)) # lower で "prod" にしてから組み立て → "myapp-prod"
  parts = split("-", local.name)                       # ["myapp", "prod"]
}

output "name" {
  value = local.name
}

output "first_part" {
  value = local.parts[0]                               # 先頭の要素 "myapp"
}

output "shout" {
  value = upper(replace(local.name, "-", "_"))         # "myapp_prod" → "MYAPP_PROD"
}
```

variable に `type` を書いていませんが、default の値から型が決まるので動きます(lesson03 では `type` を書くのが基本でした)。実行結果です。

```text
first_part = "myapp"
name = "myapp-prod"
shout = "MYAPP_PROD"
```

実務ではリソース名やバケット名を `format("%s-%s", var.project, var.env)` のように変数から組み立てるコードが最頻出です。

🔴 この5つは読めないと実務コードが追えないので、必ず手を動かして覚えましょう。

## ch02 コレクション関数（length・concat・contains ほか）

### コレクション関数とは

**コレクション**は、リスト(`[ ]`。順番付きの並び)やマップ(`{ }`。キーと値の組の集まり)のように、複数の値をまとめたものの総称です(どちらも lesson03 で見ました)。これを扱う関数を押さえます。結果は `terraform console` で実際に確かめたものです。

| 関数 | 何をするか | 例 | 結果 |
|---|---|---|---|
| `length(x)` | 要素の数 | `length(["a", "b", "c"])` | `3` |
| `concat(リスト, リスト, ...)` | リストをつないで1本に | `concat(["a", "b"], ["c"], ["d", "e"])` | `["a", "b", "c", "d", "e"]` |
| `contains(リスト, 値)` | 値が含まれるか(bool) | `contains(["80", "443"], "443")` | `true` |
| | | `contains(["80", "443"], "22")` | `false` |
| `keys(マップ)` | キーの一覧(リスト) | `keys({ zone = "1a", app = "web", env = "prod" })` | `["app", "env", "zone"]` |
| `values(マップ)` | 値の一覧(リスト) | `values({ zone = "1a", app = "web", env = "prod" })` | `["web", "prod", "1a"]` |

補足です。

- `length` はマップにも文字列にも使えます。`length({ cpu = "2", memory = "4Gi" })` は `2`(キーの数)、`length("hello")` は `5`(文字数)です
- `concat` は引数をいくつでも取れ、書いた順につなぎます
- **`keys` と `values` はどちらもキーのアルファベット順で返ります。** 書いた順(zone, app, env)ではありません。`values` は「キーをアルファベット順に並べたときの値の順」なので `["web", "prod", "1a"]` になります

### 読解例: AZ のリストを連結する

実務ではこう書かれることが多いです。

```hcl
locals {
  azs = concat(["ap-northeast-1a"], ["ap-northeast-1c"])  # 2本のリストを連結
  n   = length(local.azs)                                  # 2
  ok  = contains(local.azs, "ap-northeast-1a")             # true
}
```

`ap-northeast-1` は AWS の東京**リージョン**(データセンターがある地域)で、末尾に `a` `c` `d` が付いたものは**アベイラビリティゾーン**(AZ。リージョンの中で建物や電源が分かれたデータセンター群)です。障害に備えてサーバーを複数の AZ に分けて置くのが定石なので、AZ の一覧はリストで扱われます。「共通の AZ リストに環境ごとの追加分を `concat` する」「対象かどうかを `contains` で判定する」といった形でよく登場します。

### サンプルを1行ずつ

```hcl
variable "base_ports" {
  default = ["80", "443"]                    # 基本のポート番号(文字列のリスト)
}

variable "extra_ports" {
  default = ["8080"]                         # 追加分
}

variable "limits" {
  default = {                                # マップ
    cpu    = "2"
    memory = "4Gi"
  }
}

locals {
  ports = concat(var.base_ports, var.extra_ports)  # ["80", "443", "8080"]
}

output "port_count" {
  value = length(local.ports)                # 3
}

output "ports" {
  value = join(",", local.ports)             # ch01 の join で "80,443,8080"
}

output "has_https" {
  value = contains(local.ports, "443")       # "443" が含まれるので true
}

output "limit_keys" {
  value = join(",", keys(var.limits))        # キー一覧 ["cpu", "memory"] を join
}
```

**ポート番号**は、1台のサーバーの中で通信の受け口を区別する番号です。80 は HTTP(暗号化なしの Web)、443 は HTTPS(暗号化した Web)でよく使われます。サンプルでは文字列のリストにしているので、`contains` にも文字列の `"443"` を渡しています。

実行結果です。

```text
has_https = true
limit_keys = "cpu,memory"
port_count = 3
ports = "80,443,8080"
```

リストを output にそのまま出すと複数行の表示になるため、ここでは `join` で1行の文字列にしています。

🔴 特に keys / values の並びがアルファベット順に揃う点は、出力やリソースの並びを読むときの前提知識になります。

## ch03 lookupとmerge — タグの合成

### タグとは

AWS のリソースには**タグ**(リソースに付けるラベル。`Env = "prod"` のようなキーと値の組)を付けられます。「どの環境のものか」「どのプロジェクトのものか」を記録しておき、管理画面での検索や、費用をプロジェクト別に集計するのに使います。特に `Name` タグは AWS の管理画面で名前欄に表示されます。

Terraform ではタグを `map(string)`(キーも値も文字列のマップ。lesson03)で書きます。全リソース共通のタグと、リソースごとのタグを組み合わせるのに使うのが、このチャプターの `merge` と `lookup` です。

### merge: マップを合成する(後勝ち)

`merge(マップ1, マップ2, ...)` は複数のマップを1つにまとめます。**同じキーがあれば、後に書いたマップの値が勝ちます**。

```hcl
merge({ Env = "prod", Project = "myapp" }, { Env = "stg", Name = "myapp-logs" })
```

実際の結果です。

```text
{
  "Env" = "stg"
  "Name" = "myapp-logs"
  "Project" = "myapp"
}
```

| キー | 1つ目 | 2つ目 | 結果 |
|---|---|---|---|
| `Env` | `"prod"` | `"stg"` | `"stg"`(後勝ち) |
| `Name` | なし | `"myapp-logs"` | `"myapp-logs"` |
| `Project` | `"myapp"` | なし | `"myapp"` |

3つ以上でも同じで、`merge({ a = "1" }, { b = "2" }, { a = "3" })` は `{ a = "3", b = "2" }` になります。一番最後に書いた値が残ります。

実務ではこの形が**タグの合成**として最頻出です。全リソース共通の `local.common_tags` に、リソース個別の `Name` タグなどを重ねる書き方は、ほぼどの現場のコードにも登場します。

```hcl
tags = merge(local.common_tags, {   # 共通タグ(先)に
  Name = "myapp-api"                # 個別の Name タグ(後)を重ねる
})
```

`merge(` の第2引数として `{ ... }` のマップをその場で書いていて、閉じかっこ `})` は「マップの終わり `}` + merge の終わり `)`」です。共通を先・個別を後に書くので、同じキーがあれば個別側が優先されます。

### lookup: キーが無くても止まらない取り出し

マップの値は `マップ["キー"]` で取り出せます(lesson03)。ただし無いキーを指定すると、次のエラーで止まります。

```text
Error: Invalid index

The given key does not identify an element in this collection value.
```

`lookup(マップ, キー, 既定値)` は、キーがあればその値を、無ければ第3引数の**既定値**(代わりに使う値)を返します。

| 式 | 結果 |
|---|---|
| `lookup({ Env = "prod" }, "Env", "unknown")` | `"prod"` |
| `lookup({ Env = "prod" }, "Owner", "unknown")` | `"unknown"` |

### サンプルを1行ずつ

```hcl
variable "common_tags" {
  default = {                                  # 共通タグ
    Env     = "prod"
    Project = "myapp"
  }
}

locals {
  bucket_tags = merge(var.common_tags, {       # 共通タグに個別タグを重ねる
    Env  = "stg"                               # Env は後勝ちで "stg" に上書き
    Name = "myapp-logs"                        # Name を追加
  })
}

output "env" {
  value = local.bucket_tags["Env"]             # "stg"
}

output "owner" {
  value = lookup(local.bucket_tags, "Owner", "unknown")  # Owner は無いので "unknown"
}

output "tag_keys" {
  value = join(",", keys(local.bucket_tags))   # ch02 の keys(アルファベット順)を join
}
```

実行結果です。

```text
env = "stg"
owner = "unknown"
tag_keys = "Env,Name,Project"
```

`tag_keys` を見ると、合成後のマップには `Env` `Name` `Project` の3つのキーがあることが分かります。

🔴 「後勝ち」のルールを知らないと、環境タグを上書きしているコードを読み違えるので必ず押さえてください。

## ch04 try・coalesce・jsonencode — 壊れにくい書き方

値が「無いかもしれない」場面を安全に扱う関数と、JSON を作る関数です。

### null と空文字

「値が無い」には2種類の書き方があります。

- **null**(ヌル。「値が設定されていない」ことを表す特別な値。Python の `None` に近い)
- **空文字** `""`(長さ0の文字列。値としては存在する)

実務の variable では、「未設定」を `default = null` で表す流儀と、`default = ""` で表す流儀の両方があります。

### try: 失敗したら既定値に倒す

`try(式, 既定値)` は、1つ目の式の計算がエラーになったら、エラーで止めずに2つ目の値を返します。エラーにならなければ1つ目の式の値をそのまま返します。

ch03 で見たとおり、マップに無いキーを `["キー"]` で取り出すとエラーになります。実際に `var.cfg["port"]` を output に書いて plan すると、次のように止まります。

```text
Error: Invalid index

  on main.tf line 8, in output "port":
   8:   value = var.cfg["port"]
    ├────────────────
    │ var.cfg is map of string with 1 element

The given key does not identify an element in this collection value.
```

これを `try` で包むと止まらなくなります(`var.cfg` は `{ name = "app" }`)。

| 式 | 結果 | 理由 |
|---|---|---|
| `try(var.cfg["port"], "8080")` | `"8080"` | `port` キーが無くエラー → 既定値 |
| `try(var.cfg["name"], "none")` | `"app"` | `name` キーはあるので、その値 |

ch03 の `lookup` と似ていますが、`try` はマップのキーに限らず「エラーになる式なら何でも」既定値に倒せます。

### coalesce: 最初の「中身のある値」を選ぶ

`coalesce(a, b, ...)`(コアレス)は、引数を前から見て、**null と空文字 `""` を飛ばし**、最初に中身のある値を返します。

| 式 | 結果 |
|---|---|
| `coalesce("", "anonymous")` | `"anonymous"` |
| `coalesce(null, "", "x", "y")` | `"x"` |
| `coalesce("", "")` | エラー(`no non-null, non-empty-string arguments`。中身のある引数が1つも無い) |

「入力があればそれを、無ければ既定値を」というフォールバック(代わりの値に切り替えること)に使います。

### jsonencode: HCL の値を JSON 文字列に

**JSON**(JavaScript Object Notation。`{"name":"app"}` のような、プログラム間でデータをやり取りするための文字列の書式)を、HCL の値から作るのが `jsonencode` です。

```hcl
jsonencode({ name = "app", port = 8080, enabled = true })
```

結果は次の文字列です。

```text
"{\"enabled\":true,\"name\":\"app\",\"port\":8080}"
```

- 外側の `"..."` は「これは1つの文字列です」という印です
- `\"` は「文字列の中にある `"` という文字」を表す書き方(**エスケープ**)です。`\` を取り除いて読むと `{"enabled":true,"name":"app","port":8080}` という JSON になります
- キーはアルファベット順に並びます

AWS の **IAM ポリシー**(誰に何の操作を許可するかを書いた権限設定)などは JSON で書く決まりなので、実務では `policy = jsonencode({ ... })` の形で、HCL の書き方のまま JSON を作るコードを多く見ます。

### サンプルを1行ずつ

```hcl
variable "nickname" {
  default = ""                                   # 「未設定」を空文字で表している
}

variable "cfg" {
  type = map(string)
  default = {
    name = "app"                                 # port キーは無い
  }
}

locals {
  display = coalesce(var.nickname, "anonymous")  # "" を飛ばして "anonymous"
  port    = try(var.cfg["port"], "8080")         # port が無くエラー → "8080"
}

output "display" {
  value = local.display
}

output "port" {
  value = local.port
}

output "as_json" {
  value = jsonencode({                           # マップを JSON 文字列に
    name = var.cfg["name"]                       # "app"
    port = local.port                            # "8080"(文字列なので JSON でも "8080")
  })
}
```

実行結果です。

```text
as_json = "{\"name\":\"app\",\"port\":\"8080\"}"
display = "anonymous"
port = "8080"
```

🟡 実務コードでは `try(var.cfg["port"], "8080")` のように、キーが無くてもエラーにしない防御的な書き方として頻出します。読めれば十分ですが、意図(既定値へのフォールバック)まで取れるようにしましょう。

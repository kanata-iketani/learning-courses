# Lesson 03 variable

外から値を受け取る variable を学ぶレッスンです。基本の型から list / map / object、tfvars と validation まで、実務の `variables.tf` を読める状態を目指します。

## ch01 variableとvar.

### variable とは

ここまでのコードは、値(`"web-01"` など)をすべてコードに直接書いていました。これだと「本番用と検証用で名前だけ変えたい」ときに、コードそのものを書き換えることになります。

**variable**(外部から値を受け取るための入力口となるブロック)を使うと、値をコードの外から渡せるようになります。プログラミングでいう関数の引数に近いものです。同じコードに、本番では `"prod"`、検証では `"stg"` を渡す、という使い方ができます。

### 書き方と var. 参照

```hcl
variable "project" {     # 名前 project の variable(ラベルは1つ)
  type    = string       # 受け取る値の型: 文字列
  default = "myapp"      # 値が渡されなかったときに使う値
}

output "name" {
  value = var.project    # var.名前 で参照
}
```

| 部分 | 意味 |
|---|---|
| `variable "project"` | 種別 variable、ラベル1つ(名前)。lesson01 ch02 で見た「variable はラベル1つ」 |
| `type = string` | 受け取る値の**型**(値の種類)。`string` は文字列。型の名前は引用符で囲まない |
| `default = "myapp"` | **既定値**。外から値が渡されなかったときに使う値 |
| `var.project` | variable の値を使うときの参照の形。`var.` + 名前 |

基本の型は次の3つです(list や map などは ch02)。

| 型 | 値の例 | output での表示 |
|---|---|---|
| `string`(文字列) | `"myapp"` | `"myapp"`(引用符付き) |
| `number`(数値) | `8080` | `8080` |
| `bool`(真偽値) | `true` / `false` | `true` |

参照の形は lesson02 の resource 参照(`型.名前.属性`)と似ていますが、variable は `var.名前` だけです。属性はありません。

🔴 variable の定義と `var.` 参照は、手が覚えるまで書きましょう。

### サンプルを実行する

```hcl
variable "project" {
  type    = string
  default = "myapp"
}

variable "region" {
  type    = string
  default = "ap-northeast-1"   # AWS の東京リージョン(データセンターのある地域)を表す名前
}

output "project_name" {
  value = var.project
}

output "region_name" {
  value = var.region
}
```

何も渡さずに実行すると、default の値が使われます。

```text
project_name = "myapp"
region_name = "ap-northeast-1"
```

コマンドの `-var` オプションで値を渡すと、default より優先されます(渡し方は ch04 で詳しく見ます)。

```sh
terraform apply -var 'project=shop'   # project に "shop" を渡す
```

```text
project_name = "shop"
region_name = "ap-northeast-1"
```

project だけが渡した値になり、何も渡していない region は default のままです。

### default がないとどうなるか

default を書かない variable は「必ず外から渡す必要がある値」になります。何も渡さずに `terraform apply` すると、入力を求められます。

```text
var.project
  Enter a value:
```

入力を受け付けない実行方法(この講座の `▶ 実行` もそうです)では、次のエラーで止まります。

```text
Error: No value for required variable

  on main.tf line 1:
   1: variable "project" {

The root module input variable "project" is not set, and has no default
value. Use a -var or -var-file command line argument to provide a value for
this variable.
```

「project に値が設定されておらず、default もない。`-var` か `-var-file` で渡してください」という意味です。この講座の演習では値を渡す手段がないので、variable には必ず default を付けます。

### 型が合わない値はエラー

`type` を書いておくと、合わない値を渡したときに Terraform が止めてくれます。`type = number` の variable に `-var 'port=abc'` を渡すと、次のエラーになりました。

```text
Error: Invalid value for input variable
...
Unsuitable value for var.port set using -var="port=...": a number is
required.
```

「数値が必要です」という意味です。`-var 'port=443'` なら通ります(コマンドから渡す値は文字ですが、数値として読める文字は number に変換されます)。

### 実務の読み方

実務では variable の定義を `variables.tf` というファイルに集める流儀が一般的です。Terraform は同じフォルダの `.tf` ファイルをすべてまとめて1つのコードとして読むので、ファイルの分け方は人間が読みやすくするためのものです。

コード中の `var.xxx` を見たら、`variables.tf` を開いて「型は何か」「default はあるか(なければ外から渡している)」を確認する、が読解の第一歩です。

## ch02 型いろいろ

### 複数の値をまとめる型

ch01 の `string` / `number` / `bool` は値1つの型でした。値をまとめて持つ型として、**list** と **map** がよく使われます。

| 型 | 中身 | 値の書き方 | 要素の参照 |
|---|---|---|---|
| `list(要素の型)` | 順番付きの並び | `[80, 443]` | `var.ports[0]`(番号で) |
| `map(要素の型)` | 「キー = 値」の組の集まり | `{ env = "prod" }` | `var.tags["env"]`(キーで) |

Python を書いたことがあれば、list は Python のリスト、map は辞書(dict)に近いものです。

🔴 型の書き方と要素参照は、手が覚えるまで書きましょう。

### list(順番付きの並び)

```hcl
variable "ports" {
  type    = list(number)      # 要素がすべて number の list
  default = [80, 443, 8080]   # [ ] で囲み、要素をカンマで区切る
}
```

- `list(number)` の `( )` の中は「要素の型」です。`list(string)` なら文字列の並びになります
- 値は `[ ]` で囲み、要素を `,` で区切ります
- 要素の参照は `var.ports[番号]` です。番号は **0 から**数えます

| 参照 | 値 |
|---|---|
| `var.ports[0]` | `80` |
| `var.ports[1]` | `443` |
| `var.ports[2]` | `8080` |
| `var.ports[3]` | エラー(要素は3つしかない) |

範囲外の番号を書くと、plan の段階で次のエラーになります。

```text
Error: Invalid index
...
    │ var.ports is list of number with 3 elements

The given key does not identify an element in this collection value: the
given index is greater than or equal to the length of the collection.
```

「var.ports は要素3つの list。指定した番号が要素数以上です」という意味です。

ここでの 80・443・8080 は**ポート番号**(1台のサーバーの中で通信の受け口を区別する番号)の例です。80 は HTTP、443 は HTTPS(暗号化した HTTP)でよく使われます。

### map(キーと値の組)

```hcl
variable "tags" {
  type    = map(string)                      # 値がすべて string の map
  default = { env = "prod", team = "sre" }   # { キー = 値, キー = 値 }
}
```

- `map(string)` の `( )` の中は「値の型」です。キーは常に文字列です
- 値は `{ }` で囲み、`キー = 値` の組を `,` で区切ります。複数行に分けて書くときは `,` を省けます
- キーは `env` のように引用符なしで書けます
- 要素の参照は `var.tags["キー"]` です。`[ ]` の中のキーは引用符で囲みます

| 参照 | 値 |
|---|---|
| `var.tags["env"]` | `"prod"` |
| `var.tags["team"]` | `"sre"` |
| `var.tags["owner"]` | エラー(そのキーはない。`Invalid index`) |

実務では AWS リソースに付けるタグ(lesson02 ch04 で見た「キー = 値」のラベル)を `map(string)` でまとめることがよくあります。`sre` はインフラの運用を担当するチームの呼び名の例です。

### サンプルを実行する

```hcl
variable "debug" {
  type    = bool
  default = true
}

output "first_port" {
  value = var.ports[0]        # 0 始まり → 80
}

output "team_tag" {
  value = var.tags["team"]    # キー team の値 → "sre"
}

output "debug_mode" {
  value = var.debug           # bool の値 → true
}
```

(`ports` と `tags` の定義は上と同じです)

```text
debug_mode = true
first_port = 80
team_tag = "sre"
```

string だけが `"..."` 付きで表示され、number と bool は引用符なしで表示されます。

### list や map を丸ごと表示すると

参照で1つ取り出さずに `value = var.ports` と丸ごと output すると、次のように表示されました。

```text
all_ports = tolist([
  80,
  443,
  8080,
])
all_tags = tomap({
  "env" = "prod"
  "team" = "sre"
})
```

`tolist(...)` や `tomap(...)` は「これは list(map)型の値です」という印で、中身は `[ ]` や `{ }` の部分です。実務で output を見るとよく出てくる表示なので、読めるようにしておきましょう。

### 型が合わない値

`list(number)` に `[80, "x"]` を渡すと `a number is required`(数値が必要)というエラーになります。一方 `map(string)` に `{ env = "dev", count = 3 }` を渡すと、数値の 3 は文字列 `"3"` に変換されて通りました。数値は文字列に変換できますが、`"x"` は数値に変換できないためです。

実務では `list(string)` のサブネット ID 一覧や、`map(string)` のタグ集合が頻出なので、`[番号]` と `["キー"]` の2つの参照の形は必ず読めるようにしておきます。

## ch03 object型と実務のvariables.tf

### object 型とは

サーバーの「名前」「ポート番号」「HTTPS を使うか」のように、関係のある設定を variable 3つに分けると、どれとどれが組なのか分かりにくくなります。

**object 型**(名前付きの属性をまとめた型)を使うと、関連する設定をひとつの variable に束ねられます。

```hcl
type = object({ name = string, port = number })
```

| 部分 | 意味 |
|---|---|
| `object( )` | object 型であることを表す |
| `{ }` | 中に「属性名 = 型」を並べる |
| `name = string` | 属性 name は文字列 |
| `port = number` | 属性 port は数値 |

ch02 の map との違いは次のとおりです。

| | map | object |
|---|---|---|
| キー(属性名) | 自由。いくつあってもよい | 型で決めたものだけ |
| 値の型 | すべて同じ型 | 属性ごとに違ってよい |
| 参照 | `var.tags["env"]` | `var.db.name` |

🟡 まずは object 型の定義と参照が読めれば十分です。

### サンプルを1行ずつ

```hcl
variable "server" {
  type = object({          # object 型。以下の3つの属性を持つ
    name  = string         # name は文字列
    port  = number         # port は数値
    https = bool           # https は真偽値
  })                       # object( の閉じかっこ
  default = {              # 既定値も { } で、属性名 = 値 を並べる
    name  = "api-server"
    port  = 8080
    https = true
  }
}

output "server_name" {
  value = var.server.name  # 属性はドットでつなぐ
}

output "server_port" {
  value = var.server.port
}
```

- 複数行に分けて書くときは、属性の間の `,` を省けます(1行で書くときは `,` で区切る)
- `})` は `{` と `object(` を順に閉じています
- `var.server.name` は「variable server の name 属性」です。lesson02 の `terraform_data.origin.output` と同じく、`.` は「〜の中の」と読みます

実行結果です。

```text
server_name = "api-server"
server_port = 8080
```

`value = var.server` と丸ごと output すると、次のように表示されました。

```text
server = {
  "https" = true
  "name" = "api-server"
  "port" = 8080
}
```

### 型に合わない値

object 型の variable に値を渡すときは、型で決めた属性をすべてそろえる必要があります。`-var 'server={name="x", port=1}'` のように `https` を抜かすと、次のエラーになりました。

```text
Error: Invalid value for input variable
...
Unsuitable value for var.server set using -var="server=...": attribute
"https" is required.
```

「属性 https が必要です」という意味です。`port="abc"` のように型が違う値を入れると `a number is required` になります。

逆に、型にない属性(`owner="me"` など)を余分に入れた場合はエラーにならず、その属性は捨てられて、型で決めた3つだけが残りました。

### 実務の読解例

実務の `variables.tf` では次のような定義がよく見られます。

```hcl
variable "db" {
  description = "DB 接続設定"       # 説明文。人間向けのメモで、動作には影響しない
  type = object({
    name = string                   # DB の名前
    port = number                   # 接続するポート番号
  })
  default = { name = "app-db", port = 5432 }   # 1行で書くので , で区切る
}
```

- `description`: その variable が何のためのものかを書く説明文です。実務ではほぼ必ず書かれています
- **DB**(データベース)は、アプリのデータを保存・検索するための仕組みです。5432 は PostgreSQL(よく使われるデータベースの1つ)が標準で使うポート番号です

`var.db.port` のような参照を見たら「object 型 variable の属性アクセス」と読みます。`var.db.port` が `5432` になります。

## ch04 tfvarsと優先順位・validation

### variable に値を渡す方法

variable の値は default 以外からも渡せます。ch01 では `-var` を使いました。主な渡し方は次のとおりです。

| 渡し方 | 書き方の例 | 説明 |
|---|---|---|
| 環境変数 | `TF_VAR_env=stg terraform apply` | **環境変数**(コマンドを実行するときに OS から渡される名前付きの値)`TF_VAR_名前` |
| `terraform.tfvars` | ファイルに `env = "prod"` | 同じフォルダにあれば自動で読まれる |
| `*.auto.tfvars` | `x.auto.tfvars` など | 名前が `.auto.tfvars` で終わるファイルも自動で読まれる |
| `-var-file` | `terraform apply -var-file=prod.tfvars` | 指定したファイルを読む |
| `-var` | `terraform apply -var 'env=stg'` | コマンドで直接渡す |

**tfvars ファイル**(variable の値だけを書くファイル)は、`名前 = 値` を並べただけのファイルです。

```hcl
# terraform.tfvars(値だけを書くファイル。variable ブロックは書かない)
env = "prod"
```

variable の定義(型や default)は `.tf` ファイルに、値は tfvars ファイルに、と分けて書きます。

### 優先順位(後勝ち)

同じ variable に複数の方法で値が渡されたときは、次の順に読まれて、**後から読まれたものが勝ち**ます。

1. default(何も渡されないとき)
2. 環境変数 `TF_VAR_名前`
3. `terraform.tfvars`
4. `*.auto.tfvars`
5. `-var` と `-var-file`(コマンドに書いた順。後に書いたほうが勝つ)

実際に試した結果です(variable は `project`、default は `"myapp"`)。

| 渡したもの | 結果 |
|---|---|
| `TF_VAR_project=fromenv` だけ | `"fromenv"` |
| `TF_VAR_project=fromenv` + `terraform.tfvars` に `"fromtfvars"` | `"fromtfvars"` |
| `terraform.tfvars` + `-var-file=prod.tfvars`(中身 `"fromfile"`) | `"fromfile"` |
| `-var-file=prod.tfvars -var project=cli` | `"cli"` |
| `-var project=cli -var-file=prod.tfvars` | `"fromfile"` |

最後の2行のように、`-var` と `-var-file` は種類で強さが決まるのではなく、コマンドに書いた順で後のほうが勝ちます。

実務では環境ごとに `prod.tfvars` / `stg.tfvars` を用意し、`-var-file` で切り替える構成をよく見ます(lesson11 で扱います)。

```sh
terraform apply -var-file=stg.tfvars    # 検証環境の値で apply
```

### validation ブロック(入力チェック)

**validation ブロック**(variable の中に書く入力チェック)で、不正な値を apply の前に弾けます。

```hcl
variable "env" {
  type    = string
  default = "dev"

  validation {                                                   # 入力チェック
    condition     = contains(["dev", "stg", "prod"], var.env)    # true なら合格
    error_message = "env は dev / stg / prod のいずれかにしてください。"   # 不合格のときに出す文
  }
}
```

| 部分 | 意味 |
|---|---|
| `validation { }` | variable の本体の中に書くブロック(ラベルなし) |
| `condition` | 条件の式。true なら合格、false なら不合格 |
| `error_message` | 不合格のときに表示する文字列 |

`contains(list, 値)` は「list の中に値が含まれていれば true、なければ false」を返す**関数**(値を受け取って結果を返す組み込みの命令。lesson05)です。

| 式 | 結果 |
|---|---|
| `contains(["dev", "stg", "prod"], "dev")` | `true` |
| `contains(["dev", "stg", "prod"], "production")` | `false` |

default の `"dev"` は条件を満たすので、そのまま通ります。

```text
current_env = "dev"
```

`-var env=production` を渡すと、plan の段階で止まりました。

```text
Error: Invalid value for variable

  on main.tf line 4:
   4: variable "env" {
    ├────────────────
    │ var.env is "production"

env は dev / stg / prod のいずれかにしてください。

This was checked by the validation rule at main.tf:8,3-13.
```

`var.env is "production"` で渡された値が、その下に `error_message` に書いた文が表示されます。打ち間違い(`production` と `prod` など)で意図しない環境を作るのを防げます。

⚪ この仕組みは存在だけ知っておけば十分です。

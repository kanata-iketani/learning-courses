# Lesson 04 localsと式

ファイル内の中間変数 locals と、文字列補間・演算子・条件式を学ぶレッスンです。実務コードの名前組み立てパターンと、var / locals の使い分けの流儀まで扱います。

## ch01 localsとlocal.

### locals とは

lesson03 で見た **variable**(外から値を受け取る入力口。`var.名前` で参照)は、実行する人が `-var` や tfvars で値を差し替えられます。一方、コードの中で組み立てた値や、何度も使う値に「名前を付けておきたい」だけのこともあります。そのときに使うのが **locals**(そのモジュールの中だけで使う、名前付きの値をまとめるブロック)です。**モジュール**(Terraform のコードのひとまとまり。今は「1つのフォルダの .tf ファイル全部」と考えてよい。lesson10)の外からは見えず、外から値を差し替えることもできません。

| | variable | locals |
|---|---|---|
| 役割 | 外から受け取る入力 | 中で付けた名前(中間の値) |
| 定義 | `variable "名前" { ... }`(1つにつき1ブロック) | `locals { 名前 = 式 ... }`(1ブロックに何個でも) |
| 参照 | `var.名前` | `local.名前` |
| 外から差し替え | できる(`-var`、tfvars) | できない |
| `type` / `default` | 書ける | 書かない(右辺の式から自動で決まる) |

### 書き方を1行ずつ

```hcl
locals {                          # locals ブロックの始まり(ラベルは付けない)
  retention_days = 30             # 名前 retention_days に数値 30 を付ける
}

output "days" {
  value = local.retention_days    # 参照は local.名前(単数形)
}
```

- `locals` ブロックはラベル(`"..."` の名前)を付けず、すぐ `{` を書きます
- 本体には `名前 = 式` を何行でも並べられます。右辺の式には文字列・数値・`var.xxx`・別の `local.xxx` などが書けます
- **定義は `locals`(複数形)、参照は `local.`(単数形)**です。ここは間違えやすい所です

参照を `locals.retention_days` と複数形で書くと、Terraform は「`locals` という型のリソース」と読んでしまい、次のエラーになります(実際の表示)。

```text
Error: Reference to undeclared resource

  on main.tf line 5, in output "days":
   5:   value = locals.retention_days

A managed resource "locals" "retention_days" has not been declared in the
root module.
```

定義していない名前を `local.retention` のように参照した場合は `Reference to undeclared local value`(宣言されていない local 値への参照)というエラーになります。

### locals ブロックは何個あってもよい

`locals { }` ブロックはファイル内に何個書いてもよく、別のファイルに分けても構いません。全部合わせて1つの名前の集まりとして扱われます。ただし同じ名前を2回定義すると `Duplicate local value definition`(local 値の重複定義)というエラーになります。

実務では計算結果や共通タグなどを `locals.tf` というファイルにまとめる流儀をよく見ます。コード中の `local.xxx` を見たら、locals ブロックの定義元(多くは `locals.tf` か、同じファイルの先頭)を探すのが読解の基本です。

### サンプルを1行ずつ

```hcl
variable "team" {                  # 外からの入力 team(lesson03)
  type    = string
  default = "platform"             # 入力がなければ "platform"
}

locals {
  retention_days = 14              # 中で付けた名前(数値)
  managed_by     = "terraform"     # 中で付けた名前(文字列)
}

output "owner_team" {
  value = var.team                 # 外からの入力は var.
}

output "managed_by" {
  value = local.managed_by         # 中で付けた名前は local.
}
```

`retention_days` は定義だけして使っていません。使われない local があってもエラーにはなりません。実行結果は次のとおりです(名前のアルファベット順)。

```text
managed_by = "terraform"
owner_team = "platform"
```

このサンプルにはリソースが1つもないので、plan は `Changes to Outputs:`(output だけが変わる)と表示され、apply は `Resources: 0 added, 0 changed, 0 destroyed.` になります。output だけのコードでも apply は通ります。

### 外から差し替えられるのは variable だけ

`terraform plan -var team=sre`(lesson03 で見た、コマンドで variable の値を渡す書き方)とすると `owner_team = "sre"` に変わります。一方、`-var retention_days=1` のように local の名前を渡すと、次のエラーになります。

```text
Error: Value for undeclared variable

A variable named "retention_days" was assigned on the command line, but the
root module does not declare a variable of that name.
```

「環境ごとに変えたい値は variable、コードの中で決めてしまう値や組み立てた値は locals」と使い分けます。

🔴 locals の定義と `local.` 参照は、手が覚えるまで書きましょう。

## ch02 文字列補間と演算子

### 文字列補間 `${ }` とは

**文字列補間**(文字列の中に `${式}` と書いて、式の値を埋め込む書き方)を使うと、変数から名前を組み立てられます。Python の f 文字列 `f"{app}-{env}"` とほぼ同じものです。

```hcl
locals {
  name = "${var.app}-${var.env}"   # var.app が "web"、var.env が "dev" なら "web-dev"
}
```

記号の意味は次のとおりです。

| 部分 | 意味 |
|---|---|
| `"` ... `"` | 全体は1つの文字列 |
| `${var.app}` | `${` と `}` の間の式を評価して、その値をここに埋め込む |
| `-` | `${ }` の外なので、ただの文字 `-` |

`${ }` の中には参照だけでなく式を書けます。たとえば `"count=${3 + 4}"` は `"count=7"` になり、数値も自動で文字列に変わります。文字として `${` そのものを書きたいときは `$${` と `$` を2つ重ねます(`"$${var.env}"` は `"${var.env}"` という文字列のまま)。

注意点として、HCL では文字列どうしを `+` でつなげません。`"web" + "-dev"` は `Unsuitable value for left operand: a number is required.`(左側には数値が必要)というエラーになります。文字列をつなぐときは必ず補間(か lesson05 の `format` / `join`)を使います。

実務の Terraform ではリソース名やタグをこの形で組み立てるのが最頻出パターンで、`"${var.project}-${var.env}-web"` のような式は瞬時に読めるようになる必要があります。読むときは「`${ }` の部分を値に置き換えて、残りの文字はそのまま」と考えます。`var.project = "myapp"`、`var.env = "prod"` なら `"myapp-prod-web"` です。

### 演算子

HCL には計算や比較のための**演算子**(`+` や `==` のような、値を計算する記号)があり、locals の右辺などで使えます。実際に `terraform console`(式を1つ入力すると値を表示してくれる対話モード)で確かめた結果を載せます。

算術演算子(数値の計算):

| 式 | 結果 | 意味 |
|---|---|---|
| `20 * 2` | `40` | 掛け算 |
| `10 / 4` | `2.5` | 割り算。整数どうしでも小数になる |
| `10 % 3` | `1` | 割った余り |
| `2 + 3 * 4` | `14` | `*` `/` `%` が `+` `-` より先 |
| `(2 + 3) * 4` | `20` | `( )` の中が先 |

比較演算子(結果は `true` か `false` の **bool**(真偽値)):

| 式 | 結果 | 意味 |
|---|---|---|
| `var.env == "dev"` | `true` | 等しい(`var.env` が `"dev"` のとき) |
| `1 != 2` | `true` | 等しくない |
| `5 > 3`、`3 >= 3` | `true` | 大きい、以上(`<`、`<=` も同様) |
| `1 == "1"` | `false` | 型が違えば等しくない |
| `var.env == "Prod"` | `false` | 大文字小文字は区別する |

論理演算子(bool どうしを組み合わせる): `&&`(かつ)、`||`(または)、`!`(否定)。`5 > 3 && "a" == "b"` は `false`、`!true || 1 != 2` は `true` です。比較と論理演算子は次の ch03 の条件式でよく使います。

### サンプルを1行ずつ

```hcl
variable "app" {                      # 入力 app(default "web")
  type    = string
  default = "web"
}

variable "env" {                      # 入力 env(default "dev")
  type    = string
  default = "dev"
}

locals {
  name     = "${var.app}-${var.env}"  # "web" と "dev" を - でつないで "web-dev"
  total_gb = 20 * 2                   # 40
}

output "resource_name" {
  value = local.name
}

output "total_gb" {
  value = local.total_gb
}
```

実行結果です。文字列は `"..."` 付き、数値は引用符なしで表示されます。

```text
resource_name = "web-dev"
total_gb = 40
```

`-var env=prod` を付けて実行すれば `resource_name = "web-prod"` になります。コードを変えずに、入力だけで名前が変わるのが補間の便利なところです。

🔴 `${}` の補間は実務コードの至るところに出るので、手が覚えるまで書きましょう。

## ch03 条件式 cond ? a : b

### 条件式 `? :` とは

**条件式**(`条件 ? 真のときの値 : 偽のときの値` の形で、2つの値のどちらかを選ぶ式)は、環境によって値を切り替える定番の書き方です。**三項演算子**(項が3つある演算子)とも呼びます。Python の `"large" if env == "prod" else "small"` と同じ意味で、並び順だけが違います。

```hcl
var.env == "prod" ? "large" : "small"
```

| 部分 | 意味 |
|---|---|
| `var.env == "prod"` | 条件。ch02 で見た比較演算子で、結果は `true` か `false` |
| `?` | 「条件が true なら」の区切り |
| `"large"` | 条件が true のときの値 |
| `:` | 「そうでなければ」の区切り |
| `"small"` | 条件が false のときの値 |

`var.env` が `"prod"` なら `"large"`、`"dev"` や `"stg"` など他の値ならすべて `"small"` になります。

条件の部分には必ず bool(`true` / `false`)になる式を置きます。`var.env ? "a" : "b"` のように文字列を置くと `The condition expression must be of type bool.`(条件は bool 型でなければならない)というエラーになります。ch02 の `&&` / `||` を使って `var.env == "prod" || var.env == "stg" ? "big" : "small"` のように条件を組み合わせることもできます。

真と偽の値は同じ型にそろえるのが原則です。型が違うと Terraform が片方に合わせて変換します(例: `false ? "a" : 1` は数値ではなく文字列の `"1"` になる)。読み違いの元なので、そろえて書きましょう。

### 実務での使われ方

実務ではこう書かれることが多いです(読解例):

```hcl
locals {
  instance_type = var.env == "prod" ? "r6g.large" : "t4g.micro"
}
```

**インスタンス**は AWS で借りるサーバー1台のこと、**インスタンスタイプ**はその大きさ(CPU の数やメモリの量)を表す名前です。`r6g.large` は大きめ、`t4g.micro` はごく小さいタイプです。この1行は「本番(prod)だけ大きいサーバー、それ以外は小さく安いサーバー」という意味になります。検証環境のお金を節約しつつ、同じコードで全環境を作るための書き方です。

ほかに、後のレッスン(lesson07)で学ぶ `count = var.enabled ? 1 : 0` もよく出ます。`count` はリソースを何個作るかを指定する引数で、「`enabled` が true なら1個作る、false なら0個(作らない)」という切り替えになります。

### サンプルを1行ずつ

```hcl
variable "env" {
  type    = string
  default = "dev"                                       # 入力がなければ "dev"
}

locals {
  instance_type = var.env == "prod" ? "large" : "small" # prod なら large、それ以外は small
  is_production = var.env == "prod"                     # 比較の結果(bool)をそのまま名前に
}

output "instance_type" {
  value = local.instance_type
}

output "is_production" {
  value = local.is_production
}
```

`is_production` のように、比較の結果(bool)はそれだけで値として使えます。output に出すと `true` / `false` が引用符なしで表示されます。

default のまま実行した結果と、`-var env=prod` を付けて実行した結果を並べます。

```text
# default(env = "dev")
instance_type = "small"
is_production = false

# -var env=prod
instance_type = "large"
is_production = true
```

`env` の値1つで、2つの output がそろって切り替わっているのが分かります。

🔴 `? :` は実務コードで毎日見る形なので、手が覚えるまで書きましょう。

## ch04 varとlocalsの使い分け・命名の流儀

### 2つの流儀

var と locals の使い分けには、実務で流儀の違いがあります。どちらも動き、できあがる名前も同じです。違うのは「名前の組み立てをどこに書くか」です。

- **locals 集約派**: `name_prefix = "${var.project}-${var.env}"` のような組み立てを locals に集め、リソース側は `local.name_prefix` だけを参照する
- **var 直参照派**: リソース側で `"${var.project}-${var.env}-web"` と、使う場所ごとに組み立てる

**プレフィックス**(prefix。名前の先頭に付ける共通部分)を locals に1回だけ作っておくと、命名のルールを変えたいときに1か所直せば済みます。var 直参照は、その場で何ができるかが見えやすい反面、同じ組み立てがあちこちに散らばります。現場のコードベースでは両方が混在していることも珍しくありません。

### 読解例を1行ずつ

実務ではこう書かれることが多いです(読解例。AWS が必要なので講座では動かしません)。

```hcl
locals {
  name_prefix = "${var.project}-${var.env}"   # 例: "myapp-prod"
}

resource "aws_s3_bucket" "logs" {             # S3 バケット(AWS のファイル置き場。lesson01)
  bucket = "${local.name_prefix}-logs"        # バケット名 = 接頭辞 + "-logs" → "myapp-prod-logs"
}
```

| 行 | 意味 |
|---|---|
| `name_prefix = "${var.project}-${var.env}"` | variable 2つを `-` でつないだ接頭辞に名前を付ける(ch02 の補間) |
| `resource "aws_s3_bucket" "logs"` | 型 `aws_s3_bucket`、名前 `logs` のリソース |
| `bucket = "${local.name_prefix}-logs"` | AWS 上のバケット名。locals の接頭辞に `-logs` を足す |

同じ内容を var 直参照派で書くと `bucket = "${var.project}-${var.env}-logs"` になります。結果は同じ `"myapp-prod-logs"` です。

### 参照元のたどり方

読むときは、参照の先頭の単語で「どこを見に行くか」が決まります。

| コード中の表記 | 定義元 | よくあるファイル |
|---|---|---|
| `var.xxx` | `variable "xxx" { }` ブロック | `variables.tf`(値は tfvars。lesson03) |
| `local.xxx` | `locals { xxx = ... }` の1行 | `locals.tf` や各ファイルの先頭 |
| `型.名前.属性` | `resource "型" "名前" { }` | `main.tf` など(lesson02) |

`local.name_prefix` を見たら locals の定義元へ、そこに `var.project` があれば variables.tf へ、と1段ずつたどると、最終的な値が分かります。

### locals から locals を参照する

locals の右辺では、別の local も `local.名前` で参照できます。サンプルを1行ずつ読みます。

```hcl
variable "project" {
  type    = string
  default = "myapp"
}

variable "env" {
  type    = string
  default = "dev"
}

locals {
  name_prefix = "${var.project}-${var.env}"   # "myapp-dev"
  log_bucket  = "${local.name_prefix}-logs"   # 上の name_prefix を使って "myapp-dev-logs"
}

output "name_prefix" {
  value = local.name_prefix
}

output "log_bucket" {
  value = local.log_bucket
}
```

実行結果です(名前のアルファベット順なので `log_bucket` が先)。

```text
log_bucket = "myapp-dev-logs"
name_prefix = "myapp-dev"
```

locals の中の行の順番は関係ありません。`log_bucket` を `name_prefix` より上に書いても、Terraform が「`log_bucket` は `name_prefix` を使っている」という依存関係を見て、正しい順に計算します(実際に入れ替えても同じ結果でした)。ただし `a = local.b` と `b = local.a` のようにお互いを参照し合うと、計算の順番が決まらず `Error: Cycle: local.a (expand), local.b (expand)` というエラーになります(**Cycle** は循環参照のこと)。

🟡 どちらの流儀も読めることが目標です。

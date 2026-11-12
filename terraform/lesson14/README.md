# Lesson 14 実務コード読解2：スタイル差を読む

同じ構成でも書き手によってスタイルは変わります。フラットに resource を並べる派とモジュールに包む派の読み比べ、リファクタの痕跡(moved ブロック)の読み方を学び、最後に総合読解演習で仕上げます。

## ch01 同じ構成の2流儀読み比べ

### このレッスンで目指すこと

lesson13 では AWS の典型的な書き方を読みました。実務のコードは、書いた人やチームによって**スタイル**(同じ結果を出すための書き方のくせ・流儀)がかなり違います。中身は同じでも見た目が違うと、初めて読むときに迷います。このレッスンでは、よく出会うスタイルの差を見分けて、それぞれ「どこから読めばよいか」の手順を身につけます。

### 同じものを2つの流儀で書く

題材は「ログ用バケット」です。**S3 バケット**(AWS のファイル置き場。lesson01 で見ました)を1つ作り、アプリのログ(動作の記録)を置く場所にします。同じバケットでも、resource をそのまま並べる**フラット派**と、**モジュール**(よく使う組み立てを部品にまとめたもの。lesson10)に包む**モジュール派**がいます。

```hcl
# フラット派: リポジトリ直下に resource が並ぶ
resource "aws_s3_bucket" "logs" {
  bucket = "${var.project}-${var.env}-logs"
}

# モジュール派: 組み立てはモジュールの中
module "logs" {
  source  = "./modules/log-bucket"
  project = var.project
  env     = var.env
}
```

1行ずつ読みます。

| 行 | 意味 |
|---|---|
| `resource "aws_s3_bucket" "logs" {` | 型 `aws_s3_bucket`(S3 バケット)、名前 `logs` のリソースを定義(lesson02) |
| `bucket = "${var.project}-${var.env}-logs"` | バケット名。`${ }` は文字列の中に式の値を埋め込む書き方(lesson04)。`project = "app"`、`env = "dev"` なら `app-dev-logs` になる |
| `module "logs" {` | 名前 `logs` のモジュール呼び出し(lesson10)。ラベルは1つ |
| `source = "./modules/log-bucket"` | モジュールの中身が置いてあるフォルダ。`./` は「このファイルと同じ場所から見て」という意味 |
| `project = var.project` | モジュールの入力 `project` に、呼び出し側の変数 `var.project` を渡す |
| `env = var.env` | 同じく入力 `env` に `var.env` を渡す |

フラット派のコードにはバケット名の組み立てが直接見えています。モジュール派のコードには「何を渡したか」しか書かれておらず、バケットをどう作るかは `./modules/log-bucket` の中を開かないと分かりません。

### 流儀ごとの追い方

| | フラット派 | モジュール派 |
|---|---|---|
| resource の場所 | 呼び出し側のファイルに直接ある | `source` のフォルダの中 |
| 探し方 | `aws_s3_bucket` などの型名で **grep**(ファイルの中から文字列を探すコマンド)すれば全部見つかる | まず `module` ブロックを探し、`source` のフォルダへ移動する |
| state 上の**アドレス**(Terraform がリソースを区別する住所。lesson12) | `aws_s3_bucket.logs` | `module.logs.aws_s3_bucket.this` のように頭に `module.名前.` が付く |
| 向いている場面 | 数が少ない、1回しか使わない | 同じ組み立てを何度も使う |

モジュール派のコードは、次の順で読むと迷いません。

1. 呼び出し側の `module` ブロックで、**入力**(`source` 以外の引数。ここでは `project` と `env`)に何を渡しているかを見る
2. `source` のフォルダを開き、`variables.tf`(入力の一覧)で入力の名前と default を確認する
3. `main.tf`(本体)で、入力からどんな resource を作っているかを読む
4. `outputs.tf`(出力の一覧)で、呼び出し側に何を返しているかを見る。呼び出し側では `module.logs.出力名` で受け取る(lesson10)

ファイル名の `variables.tf` / `main.tf` / `outputs.tf` は Terraform の決まりではなく慣習です(Terraform はフォルダ内の `.tf` ファイルをすべてまとめて読みます)。1ファイルにまとめているモジュールもあります。

🟡 module ブロックを見たら「何を入力し、何を出力として受け取るか」を先に押さえるのがコツです。中身を読むのはその後です。

### サンプルを1行ずつ

サンプルでは、AWS の代わりに名前の組み立てだけを2流儀で書いています。

```hcl
variable "project" {          # 入力変数 project(lesson03)
  default = "app"             # 値を渡さなければ "app"
}

variable "env" {              # 入力変数 env
  default = "dev"
}

locals {                      # 流儀1: フラット派。その場で組み立てる(lesson04)
  flat_name = "${var.project}-${var.env}-logs"
}

module "naming" {             # 流儀2: モジュール派。名前の組み立てをモジュールに任せる
  source  = "./modules/naming"   # 中身は modules/naming フォルダ
  project = var.project          # 入力 project に "app" を渡す
  env     = var.env              # 入力 env に "dev" を渡す
}

output "flat_name" {
  value = local.flat_name     # locals の値を表示
}

output "module_name" {
  value = module.naming.bucket_name   # モジュールの出力 bucket_name を受け取って表示
}

# === file: modules/naming/main.tf ===   ← ここから下はモジュール側のファイル
variable "project" {          # モジュールの入力 project
  default = ""
}

variable "env" {              # モジュールの入力 env
  default = ""
}

output "bucket_name" {        # モジュールの出力 bucket_name
  value = "${var.project}-${var.env}-logs"   # ここでの var. はモジュール自身の入力を指す
}
```

- `# === file: ... ===` の行はこの講座の区切りで、「ここから下は別ファイル」という意味です(lesson10)
- モジュールの中の `var.project` は、呼び出し側の `var.project` とは別物です。モジュールの中では「呼び出し側から渡された値」を指します

実行すると、どちらも同じ名前になります。resource が1つもないので、plan には output の予告だけが出ます。

```text
Changes to Outputs:
  + flat_name   = "app-dev-logs"
  + module_name = "app-dev-logs"
```

```text
flat_name = "app-dev-logs"
module_name = "app-dev-logs"
```

### 手元で試すときの注意: module を足したら init

自分のパソコンで、すでに init したフォルダに `module` ブロックを後から足すと、plan で次のエラーが出ます。

```text
Error: Module not installed

This module is not yet installed. Run "terraform init" to install all modules
required by this configuration.
```

`terraform init` をもう一度実行すると `Initializing modules...` と表示されてモジュールが登録され、plan が通るようになります。実務のリポジトリでモジュールの呼び出しが増えた PR(変更の提案)を取り込んだときも同じです。この講座の「▶ 実行」は毎回 init から始めるので、このエラーは出ません。

## ch02 リファクタの痕跡を読む

### リファクタの痕跡とは

**リファクタ**(動きを変えずにコードの書き方を整え直すこと)は実務のコードでよく行われます。その跡が残っていると、「このコードは昔どう書かれていて、なぜ今の形になったか」という歴史が読み取れます。Terraform でいちばんよく見る痕跡が、count から for_each への書き換え(lesson08 ch04)と、そのときに書かれる **moved ブロック**(state に記録されたリソースのアドレスを付け替える宣言)です。

### 前提: アドレスが変わると「別物」になる

lesson12 で見たとおり、Terraform は作ったリソースを state に**アドレス**(`型.名前` などの住所)で記録しています。count と for_each では、このアドレスの形が違います。

| 書き方 | アドレスの例 | `[ ]` の中身 |
|---|---|---|
| count(lesson07) | `terraform_data.web[0]`、`terraform_data.web[1]` | 0 から始まる番号(添字) |
| for_each(lesson08) | `terraform_data.web["blue"]`、`terraform_data.web["green"]` | キー(文字列) |

`names = ["blue", "green"]` を count で作って apply した後、コードを for_each に書き換えて plan すると、実際に次の予告が出ます(抜粋)。

```text
  # terraform_data.web[0] will be destroyed
  # (because resource does not use count)
  - resource "terraform_data" "web" {
  ...
  # terraform_data.web["blue"] will be created
  + resource "terraform_data" "web" {
  ...
Plan: 2 to add, 0 to change, 2 to destroy.
```

中身は同じ blue と green なのに、Terraform は「`[0]` と `[1]` はもうコードにない(count を使わなくなった)ので消す、`["blue"]` と `["green"]` は新しいので作る」と判断します。`-` は削除、`+` は作成の印です(lesson01)。本物のサーバーやデータベースなら、いったん消えて作り直されることになり、中のデータも失われます。

### moved ブロックを1行ずつ

これを防ぐのが moved ブロックです。**aws_instance**(AWS の仮想サーバー。lesson02)の例で読みます。

```hcl
resource "aws_instance" "web" {
  for_each = toset(var.names)        # 今は for_each で作っている(toset はリストを set に。lesson08)
  # ...
}

moved {                               # アドレスの付け替えを宣言するブロック(ラベルなし)
  from = aws_instance.web[0]          # 付け替え前: count 時代のアドレス
  to   = aws_instance.web["blue"]     # 付け替え後: for_each のアドレス
}
```

- `moved` ブロックはラベルを持たず、本体に `from`(元のアドレス)と `to`(新しいアドレス)の2つだけを書きます
- `from` / `to` の右側は文字列ではなくアドレスそのものなので、`"..."` で囲みません(`["blue"]` の中のキーだけ引用符が付きます)
- 「state で `[0]` として記録しているものは、これからは `["blue"]` として扱って」という意味です。リソース本体には何もしません

先ほどの例に `[0]→["blue"]`、`[1]→["green"]` の moved を2つ足して plan すると、予告はこう変わります。

```text
  # terraform_data.web[0] has moved to terraform_data.web["blue"]
    resource "terraform_data" "web" {
        id     = "..."
        # (2 unchanged attributes hidden)
    }

  # terraform_data.web[1] has moved to terraform_data.web["green"]
  ...
Plan: 0 to add, 0 to change, 0 to destroy.
```

`has moved to` は「アドレスが付け替わるだけ」という表示で、作成も削除もありません。apply 後に `terraform state list`(state のアドレス一覧を出すコマンド)を実行すると、`terraform_data.web["blue"]` と `terraform_data.web["green"]` に変わっています。moved ブロックを残したまま次に plan しても `No changes.` で、何も起きません。

### コードに moved を見つけたときの読み方

1. `from` の形を見る。`[0]` のような番号なら「昔は count だった」、`["blue"]` のようなキーなら「昔から for_each だった」
2. `to` の形を見る。今のアドレスです。`from` と `to` を見比べると、何がどう変わったかが分かります
3. よく見る他のパターンも同じように読めます(どちらも terraform_data で同じ形を作って plan すると `has moved to` と表示され、作り直しは起きません)

| from → to | 読み取れること |
|---|---|
| `aws_s3_bucket.log` → `aws_s3_bucket.logs` | リソースの名前を変えた |
| `aws_s3_bucket.logs` → `module.logs.aws_s3_bucket.this` | フラットに書いていたものをモジュールに移した(ch01 の2流儀の移行) |

一方、`terraform state mv 元アドレス 新アドレス` という**コマンド**で state を直接書き換えて移行する方法もあります。こちらはコマンドを打つだけなので、コードには何も残りません。moved がないのにアドレスの形が変わっているコードは、この方法で移行した可能性があります。

⚪ moved の from / to を読めれば十分です。

### サンプルを1行ずつ

```hcl
variable "names" {
  default = ["blue"]                      # 名前のリスト(要素1つ)
}

resource "terraform_data" "web" {
  for_each = toset(var.names)             # リストを set にして for_each(lesson08)
  input    = "web-${each.key}"            # each.key は "blue"
}

moved {                                   # count 時代の [0] から ["blue"] への付け替えの宣言
  from = terraform_data.web[0]
  to   = terraform_data.web["blue"]
}

output "web_addresses" {
  value = join(", ", [for k in keys(terraform_data.web) : "terraform_data.web[\"${k}\"]"])
}
```

最後の output は、for_each で作ったリソースのアドレスを文字列で並べています。

| 部分 | 意味 |
|---|---|
| `terraform_data.web` | for_each のリソースは、キー → リソースの map として参照できる(lesson08 ch03) |
| `keys(...)` | map のキーだけをリストにする(lesson05)。ここでは `["blue"]` |
| `[for k in ... : ...]` | リストの各要素を k として、`:` の右の式で新しいリストを作る(lesson06) |
| `\"` | 文字列の中に `"` そのものを入れるための書き方(**エスケープ**。特別な記号を普通の文字として扱わせること) |
| `join(", ", ...)` | リストを `", "` でつないで1つの文字列にする(lesson05) |

この講座の「▶ 実行」は毎回空のフォルダで動くので、state に `[0]` は存在しません。この場合 moved は何もせず、plan は `terraform_data.web["blue"] will be created` の作成1つだけです。出力は次のとおりです。

```text
web_addresses = "terraform_data.web[\"blue\"]"
```

表示の `\"` は、文字列の中に `"` が入っていることを示しています。

## ch03 総合読解演習

### 読解の3ステップ

最後に、初めて見る実務コードを読むときの手順をまとめます。lesson11 ch03 では「リポジトリのどこから開くか」を見ました。ここでは開いたファイルの中身を読む手順です。

1. **前提値を確定する**: `variable` の `default`(または tfvars。lesson03)と `locals` を見て、`var.〜` と `local.〜` が具体的に何の値になるかを紙に書き出す
2. **何個できるかを数える**: `for_each` や `count` の対象を見て、resource がいくつ作られるかを出す。for_each なら対象の map のキーの数、count なら数字そのもの
3. **組み立て式に代入する**: `name` や `tags` の式に、1 で確定した値と 2 のキーを当てはめて、最終的な値を書き出す

### 例を1行ずつ読む

例には **ECS**(AWS でコンテナ化したアプリを動かすサービス)の `aws_ecs_service`(1つのアプリを、決まった数だけ動かし続ける設定)を使います。**コンテナ**はアプリと動かすのに必要なものを1つにまとめた箱のことです。実務では api(画面などから呼ばれる窓口のプログラム)や web(画面を返すプログラム)を、それぞれ1つの ECS サービスとして動かす構成がよくあります。

```hcl
locals {
  name_prefix = "${var.project}-${var.env}"   # 名前の頭に付ける共通部分
  services = {                                 # サービスの一覧(map。キー = サービス名)
    api = { port = 8080 }                      # api の設定。port は通信の窓口番号
    web = { port = 80 }                        # web の設定
  }
}

resource "aws_ecs_service" "this" {            # 名前 this(1種類に1個だけのときの慣習的な名前。lesson10)
  for_each = local.services                    # services の各キーごとに1つ作る(lesson08)
  name     = "${local.name_prefix}-${each.key}" # サービス名 = 共通部分 + キー
}
```

`project = "app"`、`env = "dev"` として3ステップを当てはめます。

| ステップ | 書き出す内容 |
|---|---|
| 1 前提値 | `local.name_prefix` = `"app-dev"` |
| 2 個数 | `local.services` のキーは `api` と `web` の2つ → 2個できる |
| 3 代入 | `each.key` が `api` のとき `"app-dev-api"`、`web` のとき `"app-dev-web"` |

同じ形を terraform_data で書いて plan すると、実際に次の予告になります。アドレスの `["api"]` `["web"]` が for_each のキーで、2個作られることが分かります。

```text
  # terraform_data.svc["api"] will be created
  + resource "terraform_data" "svc" {
      + input  = "app-dev-api"
  ...
  # terraform_data.svc["web"] will be created
  + resource "terraform_data" "svc" {
      + input  = "app-dev-web"
  ...
Plan: 2 to add, 0 to change, 0 to destroy.
```

この例の `port` は名前や個数には関係しません。読解では「今知りたいこと(個数・名前・タグ)に関わる値」から追い、関係のない値は後回しにして構いません。

🔴 この3ステップは実務コードを渡されたときに最初にやる作業です。演習で通しの読解を練習しましょう。

### 演習のコードで使う関数のおさらい

演習のコードには、タグ(リソースに付ける `キー = 値` のラベル。lesson13 ch01)の組み立てが出てきます。

```hcl
tags = merge(local.common_tags, { Name = "${local.name_prefix}-${each.key}" })
```

- `merge(a, b)` は2つの map を1つにまとめます(lesson05 ch03)。同じキーがあれば**後ろの map の値が勝ちます**
- `common_tags` に共通のタグを入れておき、各サービスごとに違う `Name` タグだけを足す、という実務でよく見る書き方です

確かめた実行例です(`Env` が両方にあるので、後ろの `"stg"` が残ります)。

```hcl
merge({ Project = "app", Env = "dev", ManagedBy = "terraform" }, { Name = "app-dev-api", Env = "stg" })
```

```text
merged = {
  "Env" = "stg"
  "ManagedBy" = "terraform"
  "Name" = "app-dev-api"
  "Project" = "app"
}
```

あと2つ、順番に関わる性質を押さえておきます(どちらも実際に確かめました)。

- `keys(map)` が返すキーは**アルファベット順**です。`{ web, worker, api }` の順に書いても `["api", "web", "worker"]` になります
- `jsonencode()`(値を JSON 形式の文字列にする関数。lesson05 ch04)で map を文字列にすると、キーもアルファベット順に並びます。上の map(Env なし版)なら `{"Env":"dev","ManagedBy":"terraform","Name":"app-dev-api","Project":"app"}` です。output に表示されると `"` が `\"` になります

### サンプルを1行ずつ

```hcl
locals {
  name_prefix = "${var.project}-${var.env}"   # "app-dev"
  services = {
    api = { port = 8080 }
    web = { port = 80 }
  }
}

# resource "aws_ecs_service" "this" { for_each = local.services ... } を想定
output "service_count" {
  value = length(local.services)              # map の要素数(lesson05)= キーの数 = 作られる個数
}

output "service_names" {
  value = join(", ", [for k in keys(local.services) : "${local.name_prefix}-${k}"])
  # キーごとに "app-dev-キー" を作り、", " でつなぐ
}
```

本物の `aws_ecs_service` は動かせないので、「for_each の対象が何個あるか」「名前がどうなるか」を output で計算しています。for_each の個数は対象の map の要素数と同じなので、`length(local.services)` で数えられます。

```text
service_count = 2
service_names = "app-dev-api, app-dev-web"
```

数値は `"` なしで、文字列は `"` 付きで表示されます。

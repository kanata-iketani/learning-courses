# Lesson 10 モジュール

モジュール(複数の Terraform 定義をひとまとめにして再利用する仕組み)のレッスンです。module ブロックと source の読み方、入力(variable)と出力(output)、自作モジュール、そして薄い/厚いという設計流儀までを扱います。演習は `# === file: ... ===` 区切りのマルチファイル形式です。

## ch01 moduleブロックとsource

### モジュールとは

**モジュール**(複数の Terraform 定義をひとまとめにして再利用する仕組み)は、ひとことで言うと「.tf ファイルを置いたフォルダ」です。Terraform では、1つのフォルダに置いた .tf ファイル全部が1つのまとまりとして読まれます。これまで書いてきたファイルも実は1つのモジュールで、`terraform` コマンドを実行したフォルダのモジュールを**ルートモジュール**(実行の起点になるモジュール)と呼びます。

ルートモジュールから別フォルダのモジュールを呼び出すのが `module` ブロックです。呼ばれる側を**子モジュール**と呼びます。同じ定義を何度も書かずに済み、「VPC を作るならこのモジュール」のように部品として使い回せます(**VPC** は AWS 上に作る自分専用のネットワーク)。

### source の3つの形

読解の第一歩は **source**(モジュールのコードの置き場所を示す引数)の見分けです。

| source の書き方 | 種類 | 実体の場所 |
|---|---|---|
| `./modules/naming`、`../../modules/service` | ローカル | 同じリポジトリ内のフォルダ。`./` は「今のフォルダ」、`../` は「1つ上のフォルダ」 |
| `terraform-aws-modules/vpc/aws` | レジストリ | **Terraform Registry**(公開モジュールの置き場サイト)。`作者/名前/プロバイダ` の3分割形式。`version` とセットで書く |
| `git::https://...` | git | git リポジトリを直接参照。`?ref=v1.2.0` のようにタグやブランチを指定することが多い |

```hcl
module "vpc" {                                 # 呼び出し名 vpc でモジュールを呼ぶ
  source  = "terraform-aws-modules/vpc/aws"    # レジストリの公開モジュール
  version = "5.8.1"                            # 使うバージョンを固定する
}

module "naming" {                              # 呼び出し名 naming
  source = "./modules/naming"                  # ローカル(相対パス)
}
```

`module` ブロックのラベルは1つで、これは**呼び出し名**(このコードの中でモジュールを区別する名前)です。`resource` の名前ラベルと同じく、クラウド上の名前ではありません。

🔴 実務コードで module を見たら、まず source を読んで「実体のコードがどこにあるか」を特定しましょう。

### module ブロックの中身

`module` ブロックの本体には2種類の引数が並びます。

- `source`、`version` など Terraform 自身が決めている引数
- それ以外(`name = "terraform"` など): 子モジュールの `variable`(lesson03 で見た入力変数)に渡す値

つまり `name = "terraform"` は「子モジュールの `variable "name"` に `"terraform"` を入れる」という意味です。子モジュールの output は `module.呼び出し名.output名` で受け取ります。`.` で区切って「module の、hello の、message」と順にたどる書き方で、lesson02 で見たリソース参照 `型.名前.属性` と同じ形です。

### サンプルを1行ずつ

この講座のエディタでは、`# === file: modules/greet/main.tf ===` という区切り行から下が別ファイル(`modules/greet/main.tf`)として保存されます。つまりサンプルは次の2ファイル構成です。

```text
main.tf                ← ルートモジュール(呼び出し側)
modules/
  greet/main.tf        ← 子モジュール(呼ばれる側)
```

```hcl
# --- main.tf(呼び出し側) ---
module "hello" {                 # 呼び出し名 hello
  source = "./modules/greet"     # ./ 始まり = ローカル。modules/greet フォルダが実体
  name   = "terraform"           # 子モジュールの variable "name" へ渡す値
}

output "message" {
  value = module.hello.message   # hello モジュールの output "message" を受け取る
}

# --- modules/greet/main.tf(子モジュール) ---
variable "name" {                # 入力: 呼び出し側から name を受け取る
  type = string
}

output "message" {               # 出力: 呼び出し側へ返す値
  value = "hello, ${var.name}"   # ${ } は文字列の中に式の値を埋め込む書き方
}
```

### init でモジュールを読み込む

モジュールを使うときは `terraform init` が必要です。実行すると、モジュールの読み込みが表示されます。

```text
Initializing modules...
- hello in modules/greet
```

「呼び出し名 hello は modules/greet にある」と記録されています。レジストリや git のモジュールは、このとき `.terraform/modules/` の下にダウンロードされます。ローカルモジュールはコピーされず、場所が記録されるだけです。

`module` ブロックを足したのに init し直さずに plan すると、次のエラーになります。

```text
Error: Module not installed

This module is not yet installed. Run "terraform init" to install all modules
required by this configuration.
```

(この講座の ▶実行は毎回 init から始めるので、このエラーは出ません。手元で試すときに覚えておけば十分です)

apply すると次のようになります。子モジュールにはリソースがないので、作られるものは0個で、output だけが表示されます。

```text
Apply complete! Resources: 0 added, 0 changed, 0 destroyed.

Outputs:

message = "hello, terraform"
```

## ch02 モジュールの入力と出力

### モジュールの境界は variable と output だけ

モジュールの**境界**(外部とやりとりできる接点)は、variable(入力)と output(出力)の2つだけです。

```text
呼び出し側(main.tf)                         子モジュール(modules/tagger/main.tf)
module "tags" {
  env   = "stg"     ───── 入力 ─────▶      variable "env"
  owner = "sre"     ───── 入力 ─────▶      variable "owner"
}                                            locals { tag_line = ... }   ← 内部だけの値
module.tags.tag_line ◀──── 出力 ─────      output "tag_line"
```

- 呼び出し側は module ブロックの引数で、子モジュールの variable に値を渡します
- 結果は `module.呼び出し名.output名` で受け取ります
- 子モジュールの中のリソースや locals(lesson04 で見たファイル内だけの名前付きの値)は、外から直接参照できません。output で公開されたものだけが見えます

この「中身を隠して、入口と出口だけを決める」作りのおかげで、使う側は子モジュールの中身を全部読まなくても、variable と output を見れば使い方がわかります。

### サンプルを1行ずつ

```hcl
# --- main.tf(呼び出し側) ---
module "tags" {
  source = "./modules/tagger"
  env    = "stg"                   # → 子の variable "env" へ
  owner  = "sre"                   # → 子の variable "owner" へ
}

output "tag_line" {
  value = module.tags.tag_line     # ← 子の output "tag_line" から
}

# --- modules/tagger/main.tf(子モジュール) ---
variable "env"   { type = string } # 入力1
variable "owner" { type = string } # 入力2

locals {
  tag_line = "env=${var.env} owner=${var.owner}"  # 内部で文字列を組み立てる
}

output "tag_line" {
  value = local.tag_line           # 内部の値を output で外へ公開する
}
```

呼び出し側と子モジュールに同じ `tag_line` という名前の output がありますが、別物です。子の output は `module.tags.tag_line` として呼び出し側に届き、それを呼び出し側の output が `terraform output` に表示しています。

```text
tag_line = "env=stg owner=sre"
```

### 境界を越えようとするとエラーになる

子モジュールの locals を外から `module.tags.local.tag_line` と参照すると、次のエラーになります。

```text
Error: Unsupported attribute

  on main.tf line 14, in output "x":
  14:   value = module.tags.local.tag_line
    ├────────────────
    │ module.tags is a object

This object does not have an attribute named "local".
```

`module.tags` は「子の output だけを持つ object(名前付きの値の集まり)」なので、`local` という属性は存在しない、という意味です。

入力側でも、子の variable と合わないとエラーになります。以下は ch01 の greet モジュールで試した例です。default(lesson03 で見た既定値)のない variable `name` に値を渡し忘れると:

```text
Error: Missing required argument

The argument "name" is required, but no definition was found.
```

子に存在しない variable 名 `age` を渡すと:

```text
Error: Unsupported argument

An argument named "age" is not expected here.
```

### 子モジュールのリソースの住所

子モジュールの中にリソースがあると、plan や state では `module.呼び出し名.型.名前` という**アドレス**(Terraform 内でのリソースの住所)で表示されます。たとえば `modules/box` に `resource "terraform_data" "this"` を置いて `module "box"` で呼ぶと、plan はこうなります。

```text
  # module.box.terraform_data.this will be created
  + resource "terraform_data" "this" {
      + id     = (known after apply)
      + input  = "a"
      + output = (known after apply)
    }
```

実務の plan で `module.xxx.` から始まる行を見たら「xxx モジュールの中のリソース」と読みます。モジュール内のリソース名に `this` がよく使われるのは、「このモジュールが作る主役の1個」という慣習です。

### 実務コードでの突き合わせ

```hcl
module "vpc" {
  source = "./modules/vpc"
  cidr   = "10.0.0.0/16"        # → モジュール側 variable "cidr" へ
}

resource "aws_subnet" "app" {
  vpc_id = module.vpc.vpc_id    # ← モジュール側 output "vpc_id" から
}
```

- `cidr` は **CIDR**(`10.0.0.0/16` のように IP アドレスの範囲を表す書き方。`/16` は先頭16ビットが固定という意味で、約6.5万個のアドレス)を渡しています
- `aws_subnet` は **サブネット**(VPC の中をさらに区切った小さなネットワーク)です。どの VPC の中に作るかを `vpc_id` で指定する必要があり、その ID をモジュールの output から受け取っています

実務のモジュールは `variables.tf`(variable を集めたファイル)・`main.tf`(リソース本体)・`outputs.tf`(output を集めたファイル)に分かれていることが多いです。

🔴 実務の読解では「module ブロックの引数 ↔ モジュール側の variables.tf」「module.xxx.yyy ↔ モジュール側の outputs.tf」を突き合わせるのが基本動作です。

## ch03 モジュールを自作する

### 自作の手順は「フォルダを作って置くだけ」

モジュールの自作に特別な宣言はいりません。手順は次の3つです。

1. フォルダを作る(例: `modules/naming/`)
2. その中の .tf ファイルに variable(入力)・locals(内部の計算)・output(出力)を書く
3. 呼び出し側から `module` ブロックの `source = "./modules/naming"` で呼ぶ

フォルダ名やファイル名に決まりはありませんが、実務では `modules/` の下に用途別のフォルダを並べる構成がよく使われます。

### naming モジュール

実務でよくあるのが **naming モジュール**(命名規約を1か所に集約するモジュール)です。**命名規約**とは「リソース名は `アプリ名-環境名` で付ける」のような、チーム内の名前の付け方の決まりです。

規約を各リソースに直接書くと、`"api-stg-logs"`、`"api-stg-jobs"` のように同じ組み立てがあちこちに散らばります。naming モジュールにまとめれば、全リソースに同じ規則が一貫して適用され、規約が変わってもモジュール1か所を直せば済みます。

```hcl
module "naming" {
  source = "./modules/naming"
  env    = "prod"                    # 環境名(prod = 本番、stg = 検証)
  app    = "myapp"                 # アプリ名
}

# 使う側は module.naming.bucket_name などを参照するだけ
# bucket = module.naming.bucket_name # => "myapp-prod-logs"
```

**prod**(production。本番環境)と **stg**(staging。本番前に動作を確かめる検証環境)は、実務コードで頻繁に見る環境名の略です。

### サンプルを1行ずつ

```hcl
# --- main.tf(呼び出し側) ---
module "naming" {
  source = "./modules/naming"
  env    = "stg"                     # → variable "env"
  app    = "api"                     # → variable "app"
}

output "prefix" {
  value = module.naming.prefix       # ← output "prefix"
}

# --- modules/naming/main.tf(自作モジュール) ---
variable "env" { type = string }     # 入力: 環境名
variable "app" { type = string }     # 入力: アプリ名

output "prefix" {
  value = "${var.app}-${var.env}"    # "api" と "-" と "stg" をつなげて "api-stg"
}
```

```text
prefix = "api-stg"
```

`"${var.app}-${var.env}"` は lesson04 で見た文字列補間です。`${ }` の中の式の値がその場所に埋め込まれ、間の `-` はそのまま文字として残ります。

### 規約を直すと全リソースが追従する

naming モジュールの出力を、2つのリソースの名前に使ってみます。

```hcl
resource "terraform_data" "bucket" {
  input = "${module.naming.prefix}-logs"   # "api-stg" + "-logs"
}

resource "terraform_data" "queue" {
  input = "${module.naming.prefix}-jobs"   # "api-stg" + "-jobs"
}
```

apply すると `bucket = "api-stg-logs"`、`queue = "api-stg-jobs"` になります。ここで命名規約を「環境名-アプリ名」に変えるため、モジュール側の1行だけを `"${var.env}-${var.app}"` に直して plan すると、次の予告が出ました。

```text
  # terraform_data.bucket will be updated in-place
  ~ resource "terraform_data" "bucket" {
        id     = "..."
      ~ input  = "api-stg-logs" -> "stg-api-logs"
      ~ output = "api-stg-logs" -> (known after apply)
    }

  # terraform_data.queue will be updated in-place
  ~ resource "terraform_data" "queue" {
        id     = "..."
      ~ input  = "api-stg-jobs" -> "stg-api-jobs"
      ~ output = "api-stg-jobs" -> (known after apply)
    }

Plan: 0 to add, 2 to change, 0 to destroy.
```

- `~` は「変更する」の印、`->` は「変更前 -> 変更後」です
- `updated in-place` は作り直さずにその場で値を書き換える、という意味です

呼び出し側のコードは1文字も変えていないのに、両方の名前が新しい規約に変わりました。これが「規約をモジュールに閉じ込める」効果です。なお、ローカルモジュールの中身を書き換えただけなら `terraform init` のやり直しは不要でした。init が必要なのは、`module` ブロックを足したときや `source` を変えたときです。

(本物のクラウドでは、名前の変更はリソースの作り直しになることが多いので、実務で命名規約を変えるときは plan をよく確認します)

🔴 「規約や決まりごとをモジュールに閉じ込める」という発想は、実務コード読解でも設計でも要になります。

## ch04 薄いモジュールvs厚いモジュール

### 2つの流儀

実務のモジュール設計には流儀の対立があります。

- **薄いモジュール**(リソース1個を包み、引数をほぼ素通しするモジュール)
- **厚いモジュール**(複数リソースと社内規約を焼き込み、少ない入力で多くを作るモジュール)

「素通し」とは、受け取った variable をそのままリソースの引数に渡すことです。「焼き込む」とは、呼び出し側に選ばせずにモジュールの中で値を決め打ちしておくことです。

### 薄いモジュールの例

```hcl
# modules/s3_bucket/main.tf(薄いモジュールのイメージ)
variable "bucket"        { type = string }  # バケット名
variable "force_destroy" { type = bool }    # 中身があっても削除できるか
variable "tags"          { type = map(string) }
# ...このような variable が十数個続く

resource "aws_s3_bucket" "this" {           # リソースは1個だけ
  bucket        = var.bucket                # 受け取った値をそのまま渡す(素通し)
  force_destroy = var.force_destroy
  tags          = var.tags
}
```

(**S3 バケット**は AWS のファイル置き場1つ分。`map(string)` は lesson03 で見た「キーも値も文字列のマップ」型です)

- 長所: 何でも設定できて柔軟。中で何が起きているかが追いやすい
- 短所: 呼び出し側が全部の値を書くので、記述が長くなる。規約は呼び出し側が守る必要がある

### 厚いモジュールの例

```hcl
# 厚いモジュールの典型: 入力2個で VPC + サブネット + NAT までまとめて作る
module "network" {
  source = "./modules/network"
  env    = "prod"            # 環境名
  cidr   = "10.0.0.0/16"     # ネットワーク全体の IP アドレス範囲(lesson10 ch02 で見た CIDR)
}
```

モジュールの中では、VPC(自分専用のネットワーク)、サブネット(その中の区画)、**NAT ゲートウェイ**(内側のサーバーがインターネットへ出ていくための出口)など十数個のリソースが、社内で決めた設定で作られます。

- 長所: 少ない入力で規約どおりの構成ができ、記述が短い。規約を強制できる
- 短所: 規約から外れる個別調整(「この環境だけ NAT を省きたい」など)が難しい。variable を足すたびにモジュールが複雑になる

どちらが正しいということはなく、チームの方針の違いです。読解ではまず「このリポジトリはどちら寄りか」を把握します。

### 見分け方: variable の数と resource の数の比

🟡 読解時は「variable の数」と「中の resource の数」の比を見ると流儀を推測できます。variable が多く resource が1個なら薄い、その逆なら厚いモジュールです。

| モジュール | variable の数 | resource の数 | 推測 |
|---|---|---|---|
| s3_bucket | 14 | 1 | 薄い |
| network(vpc) | 4 | 12 | 厚い |

### サンプルを1行ずつ

サンプルは、この判定ロジックを条件式で書いたものです。

```hcl
locals {
  input_count    = 14   # 読解して数えた variable の数
  resource_count = 1    # 読解して数えた resource の数

  # 条件 ? 真のときの値 : 偽のときの値(lesson04 の条件式)
  style = local.resource_count > local.input_count ? "thick" : "thin"
}

output "style" {
  value = local.style
}
```

- `>` は「左が右より大きい」の比較で、結果は true か false です
- `1 > 14` は false なので、`:` の右側 `"thin"` が選ばれます

```text
style = "thin"
```

### 演習の前に: マップの for 式と入れ子の値

演習では、lesson06 で見たマップの for 式を使います。

```hcl
modules = {
  s3_bucket = { inputs = 14, resources = 1 }   # 値が object(名前付きの値の集まり)
  vpc       = { inputs = 4, resources = 12 }
}

[for k, v in local.modules : "${k}:..."]
```

- `for k, v in マップ` は、`k` にキー(`"s3_bucket"` など)、`v` に値(`{ inputs = 14, resources = 1 }`)が入って順に回ります。順番はキーのアルファベット順です
- 値の中身は `v.inputs`、`v.resources` のように `.` でたどって取り出します
- `${ }` の中には条件式もそのまま書けます。`"${v.inputs > 10 ? "many" : "few"}"` のように、外側の `"..."` の中で内側の `"thick"` を使ってかまいません
- できたリストは lesson05 で見た `join(", ", リスト)` で、`, ` を挟んだ1つの文字列にまとめます

# Lesson 11 環境分割の流儀

同じ構成を prod / stg など複数環境に展開するときの流儀を学ぶレッスンです。ディレクトリ分割・tfvars・workspace の 3 方式の見分け方を押さえ、最後に初見のリポジトリを読む手順をチェックリスト化します。

## ch01 ディレクトリ分割方式

### なぜ環境を分けるのか

実務では、同じシステムを複数の**環境**(用途ごとに分けた、同じ構成のインフラ一式)に作ります。よく見る環境名は次のとおりです。

| 環境名 | 正式名 | 用途 |
|---|---|---|
| `prod` | production | 本番。実際のお客さんが使う |
| `stg` | staging | 検証。本番とほぼ同じ構成で、リリース前の確認に使う |
| `dev` | development | 開発。開発者が自由に試す |

構成はほぼ同じですが、「本番だけサーバーを大きくする」「検証はログを短期間で消す」のような設定差があります。この「ほぼ同じコードを、少しずつ違う値で複数回使う」をどう書くかが**環境分割**の流儀で、このレッスンでは代表的な3つ(ディレクトリ分割・tfvars・workspace)を見ます。

### ディレクトリ分割方式

同じ構成を prod / stg に展開する最も一般的な流儀が**ディレクトリ分割方式**(環境ごとにディレクトリを分け、それぞれが同じモジュールを呼ぶ構成)です。

```text
environments/
  prod/main.tf      # module "service" { source = "../../modules/service"  env = "prod" }
  stg/main.tf       # module "service" { source = "../../modules/service"  env = "stg" }
modules/
  service/main.tf   # 共通ロジック本体
```

- `environments/prod` と `environments/stg` がそれぞれ**ルートモジュール**(lesson10 で見た、terraform コマンドを実行するフォルダ)です。`cd environments/prod` してから `terraform apply` のように、環境ごとのフォルダで実行します
- `source = "../../modules/service"` の `../../` は「2つ上のフォルダ」です。`environments/prod` から2つ上がるとリポジトリの一番上に出て、そこから `modules/service` を指します
- 共通の中身は `modules/service` に1つだけ置き、各環境は「どんな値で呼ぶか」だけを書きます

### 2つの環境ディレクトリの diff を取る

実際にこの構成を作り、prod と stg の main.tf を `diff -u`(2つのファイルの違いを表示するコマンド)で比べると、こうなりました。

```text
--- environments/prod/main.tf
+++ environments/stg/main.tf
@@ -1,6 +1,6 @@
 module "service" {
   source = "../../modules/service"
-  env    = "prod"
+  env    = "stg"
 }
```

`-` の行が prod だけにある行、`+` の行が stg だけにある行です。違いは module へ渡す引数(env 名やスペックなど)だけに現れます。

🟡 読解時は2つの環境ディレクトリの diff を取るのが近道で、そこに現れた差分こそが「環境ごとの設定差」です。

### state も環境ごとに分かれる

それぞれのフォルダで init → apply すると、フォルダごとに別の **state**(lesson01 で見た、管理中のリソースの記録ファイル)ができます。

```text
environments/prod/terraform.tfstate   ← prod の記録
environments/stg/terraform.tfstate    ← stg の記録
```

stg で apply しても prod の state には触れないので、「検証のつもりで本番を壊す」事故が起きにくいのがこの方式の強みです。一方、環境の数だけほぼ同じ main.tf が並ぶので、共通部分の変更は全環境のファイルに入れる必要があります。

### サンプルを1行ずつ

この講座の ▶実行は1つのフォルダでしか動かないので、サンプルでは prod と stg の2つの呼び出しを1ファイルにまとめています。実務では別々のフォルダに置かれる2つの呼び出しだと思って読んでください。

```hcl
module "prod" {                      # 実務なら environments/prod/main.tf の中身
  source = "./modules/service"
  env    = "prod"
}

module "stg" {                       # 実務なら environments/stg/main.tf の中身
  source = "./modules/service"       # 同じモジュールを呼ぶ
  env    = "stg"                     # 違うのはここだけ
}

output "prod_name" { value = module.prod.name }
output "stg_name"  { value = module.stg.name }

# --- modules/service/main.tf ---
variable "env" { type = string }

output "name" {
  value = "app-${var.env}"           # env を名前に埋め込む
}
```

```text
prod_name = "app-prod"
stg_name = "app-stg"
```

1つのモジュールでも、渡す env が違えば結果が変わります。

### 演習の前に: 条件式でスペックを出し分ける

演習のモジュールには、env によって**インスタンスタイプ**(AWS の仮想サーバー EC2 の性能の種類。`m5.large` は中くらい、`t3.small` は小さめ)を変える output があります。

```hcl
output "instance_type" {
  value = var.env == "prod" ? "m5.large" : "t3.small"
}
```

`==` は「等しいか」の比較、`条件 ? 真のとき : 偽のとき` は lesson04 で見た条件式です。env が `"prod"` なら `"m5.large"`、それ以外なら `"t3.small"` になります。

## ch02 tfvars方式とworkspace方式

ディレクトリを分けず、1つのコードで複数環境を扱う流儀が2つあります。

### tfvars 方式

**tfvars 方式**(環境ごとの変数ファイルを `-var-file=prod.tfvars` のように差し替えて apply する方式)は、ルートに `prod.tfvars` / `stg.tfvars` が並んでいるのが目印です。**tfvars ファイル**は lesson03 で見た「variable の値だけを書くファイル」です。

```text
main.tf        # variable "env" と variable "min_size" を受け取るコード
prod.tfvars    # env = "prod" / min_size = 4
stg.tfvars     # env = "stg"  / min_size = 1
```

```hcl
# main.tf
variable "env"      { type = string }   # default なし = 必ず外から渡す
variable "min_size" { type = number }

output "summary" {
  value = "${var.env}: min_size=${var.min_size}"
}
```

```hcl
# stg.tfvars(変数名 = 値 を並べるだけ)
env      = "stg"
min_size = 1
```

`terraform apply -var-file=stg.tfvars` で実行すると、stg.tfvars の値が variable に入ります。

```text
summary = "stg: min_size=1"
```

同じフォルダで `-var-file=prod.tfvars` に替えて plan すると、同じ output が prod の値に置き換わる予告が出ました。

```text
Changes to Outputs:
  ~ summary = "stg: min_size=1" -> "prod: min_size=4"
```

ここで注意点があります。1つのフォルダには state が1つしかないので、tfvars を替えただけでは「stg の記録を prod の値で上書きする」ことになります。そのため実務の tfvars 方式では、state の置き場(lesson12 で扱うバックエンド)も環境ごとに切り替える設定とセットで使います。また `-var-file` を付け忘れると、default のない variable は値がなくエラー(`No value for required variable`)になるか、値の入力を求められます。

### workspace 方式

**workspace 方式**(`terraform workspace` コマンドで state を切り替える方式)は、コード内の `terraform.workspace` 参照と、それを使った条件式が目印です。**workspace** は、1つのフォルダの中に state を名前付きで複数持てる仕組みです。

```hcl
# workspace 方式の典型: 環境名で設定値を出し分ける
locals {
  env      = terraform.workspace             # 今いる workspace の名前("prod" や "stg")
  min_size = local.env == "prod" ? 4 : 1     # prod なら 4、それ以外は 1
}
```

実際に動かすとこうなります。最初は `default` という workspace にいます。

```sh
terraform workspace show        # 今の workspace 名を表示 → default
terraform apply                 # env = "default", min_size = 1
terraform workspace new prod    # prod を作って切り替える
terraform apply                 # env = "prod", min_size = 4
```

`workspace new` の直後には次のメッセージが出ます。

```text
Created and switched to workspace "prod"!

You're now on a new, empty workspace. Workspaces isolate their state,
so if you run "terraform plan" Terraform will not see any existing state
for this configuration.
```

「新しい空の workspace で、state は分離されている」という意味です。手元では state ファイルが次のように分かれていました。

```text
terraform.tfstate                    ← default の state
terraform.tfstate.d/prod/terraform.tfstate   ← prod の state
```

`terraform workspace list` は一覧を出し、今いる workspace に `*` が付きます。workspace の切り替えを忘れて apply すると別環境に反映されてしまうので、どの workspace にいるかを常に確認する運用が必要です。

### 3方式の目印のまとめ

| 方式 | リポジトリの目印 | 環境の切り替え方 |
|---|---|---|
| ディレクトリ分割(ch01) | `environments/prod/`、`environments/stg/` | 実行するフォルダを変える |
| tfvars | `prod.tfvars`、`stg.tfvars` | `-var-file=` を変える |
| workspace | `terraform.workspace` の参照 | `terraform workspace select 名前` |

🟡 どちらの方式でも「env 名で条件分岐して設定値を出し分ける」パターンが核になるので、条件式を読めることが重要です。

### サンプルを1行ずつ

この講座の ▶実行では workspace を切り替えられないので、サンプルは `terraform.workspace` の代わりに variable で環境名を受け取ります。

```hcl
variable "env" {
  type    = string
  default = "prod"                       # 値を渡さなければ "prod"
}

locals {
  is_prod  = var.env == "prod"           # 比較の結果 true / false を名前付きで持つ
  min_size = local.is_prod ? 4 : 1       # true なら 4、false なら 1
}

output "env"      { value = var.env }
output "min_size" { value = local.min_size }
```

```text
env = "prod"
min_size = 4
```

`is_prod` のように比較結果を locals に名前を付けて置くと、同じ比較を何度も書かずに済み、読む人にも意図が伝わります。実務コードでもよく見る書き方です。default を `"stg"` に変えると `min_size = 1` になります。

## ch03 初見のリポジトリを読む手順

### 読む順番を固定する

初見の Terraform リポジトリは、読む順番を固定すると迷いません。まずディレクトリ構成を見て分割方式(ch01・ch02 で見た `environments/` の有無、tfvars の有無)を判定し、その後は次の順に読みます。

```text
読む順チェックリスト
1. backend  : state はどこか(このコードの守備範囲)
2. provider : どのクラウド・リージョン・アカウントか
3. variables: 何が環境ごとに変わるのか
4. main     : 実際に何を作っているのか
```

🔴 「いきなり resource を読まず、backend と variables で全体の枠を掴んでから本体へ」が実務読解の鉄則です。

### 1. backend: state はどこか

**backend**(バックエンド。state ファイルの置き場所の設定)は、`terraform` ブロックの中に書かれています。実務では state をチームで共有するため、手元ではなく S3(AWS のファイル置き場)などに置きます。詳しくは lesson12 で扱います。

```hcl
terraform {                              # Terraform 自体の設定をまとめるブロック
  backend "s3" {                         # state を S3 に置く
    bucket = "example-tfstate"           # 置き場の S3 バケット名
    key    = "prod/network.tfstate"      # バケット内のファイルパス
    region = "ap-northeast-1"            # バケットがあるリージョン(東京)
  }
}
```

`key` を見ると、このフォルダが「prod 環境の network 部分」を管理していると推測できます。1つの state が管理する範囲がそのまま「このコードの守備範囲」なので、最初に確認します。

### 2. provider: どのクラウド・リージョン・アカウントか

**provider**(プロバイダ。AWS などを操作するためのプラグイン。lesson01 で名前だけ出ました)の設定には、操作先の情報が書かれています。

```hcl
provider "aws" {                         # AWS を操作する
  region              = "ap-northeast-1" # 操作するリージョン
  allowed_account_ids = ["123456789012"] # このアカウント以外では動かさない安全装置
}
```

- **リージョン**は AWS のデータセンターがある地域です。`ap-northeast-1` は東京、`us-east-1` はバージニア北部です
- **アカウント ID** は AWS アカウント(契約の単位)を表す12桁の番号です。本番用と検証用でアカウントを分けることが多く、ここを見れば「どの環境向けのコードか」がわかります

### 3. variables と tfvars: 何が環境ごとに変わるのか

`variables.tf` の variable 一覧と、`*.tfvars` の値を見ます。ch01 の diff と同じく、環境ごとに値が違う項目が「環境差」です。default のない variable は「必ず外から渡される値」なので、tfvars のどこで渡しているかを探します。

### 4. main と module: 実際に何を作っているのか

ここで初めて resource と module を読みます。module があれば、lesson10 で見たとおり source で実体の場所を特定し、引数 ↔ variables.tf、`module.xxx.yyy` ↔ outputs.tf を突き合わせます。

### サンプルを1行ずつ

サンプルは、このチェックリストを番号付きで整形するコードです。lesson06 で見た「インデックス付き for 式」を使います。

```hcl
locals {
  steps = ["backend", "provider", "variables", "main"]     # 4要素のリスト

  numbered = [for i, s in local.steps : "${i + 1}. ${s}"]
}

output "first_step" { value = local.numbered[0] }    # リストの先頭(0番目)
output "step_count" { value = length(local.steps) }  # 要素数
```

- `for i, s in リスト` と変数を2つ書くと、`i` に**インデックス**(要素の位置番号。0 始まり)、`s` に要素の値が入ります
- `${i + 1}` は、0 始まりの番号に 1 を足して、人が読む 1 始まりの番号にしています
- `[0]` はリストの0番目(先頭)を取り出す書き方、`length()` は lesson05 で見た要素数を返す関数です

for 式が回る様子を表にするとこうなります。

| i | s | 作られる文字列 |
|---|---|---|
| 0 | `"backend"` | `"1. backend"` |
| 1 | `"provider"` | `"2. provider"` |
| 2 | `"variables"` | `"3. variables"` |
| 3 | `"main"` | `"4. main"` |

```text
first_step = "1. backend"
step_count = 4
```

演習では、区切りを `. ` ではなく `:` にした `"1:backend"` 形式で作り、lesson05 で見た `join(", ", リスト)` で1行にまとめます。

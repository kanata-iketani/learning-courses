# Lesson 11 環境分割の流儀

同じ構成を prod / stg など複数環境に展開するときの流儀を学ぶレッスンです。ディレクトリ分割・tfvars・workspace の 3 方式の見分け方を押さえ、最後に初見のリポジトリを読む手順をチェックリスト化します。

## ch01 ディレクトリ分割方式

同じ構成を prod / stg に展開する最も一般的な流儀が**ディレクトリ分割方式**(環境ごとにディレクトリを分け、それぞれが同じモジュールを呼ぶ構成)です。`environments/prod` と `environments/stg` の main.tf はほぼ同じで、違いは module へ渡す引数(env 名やスペックなど)だけに現れます。🟡 読解時は 2 つの環境ディレクトリの diff を取るのが近道で、そこに現れた差分こそが「環境ごとの設定差」です。

```text
environments/
  prod/main.tf  # module "service" { source = "../../modules/service"  env = "prod" }
  stg/main.tf   # module "service" { source = "../../modules/service"  env = "stg" }
modules/
  service/main.tf # 共通ロジック本体
```

## ch02 tfvars方式とworkspace方式

ディレクトリを分けず 1 つのコードで複数環境を扱う流儀が 2 つあります。**tfvars 方式**(環境ごとの変数ファイルを `-var-file=prod.tfvars` のように差し替えて apply する方式)は、ルートに `prod.tfvars` / `stg.tfvars` が並んでいるのが目印です。**workspace 方式**(`terraform workspace` コマンドで state を切り替える方式)は、コード内の `terraform.workspace` 参照と、それを使った条件式が目印です。🟡 どちらの方式でも「env 名で条件分岐して設定値を出し分ける」パターンが核になるので、条件式を読めることが重要です。

```hcl
# workspace 方式の典型: 環境名で設定値を出し分ける
locals {
  env      = terraform.workspace # "prod" や "stg"
  min_size = local.env == "prod" ? 4 : 1
}
```

## ch03 初見のリポジトリを読む手順

初見の Terraform リポジトリは、読む順番を固定すると迷いません。まずディレクトリ構成を見て分割方式(environments/ の有無、tfvars の有無)を判定し、その後は 1. backend(state の置き場。= このディレクトリが管理する範囲)、2. provider(どのクラウド・リージョン・アカウントか)、3. variables と tfvars(何が環境ごとに変わるのか)、4. main と module(実際に何を作っているのか)の順に読みます。🔴 「いきなり resource を読まず、backend と variables で全体の枠を掴んでから本体へ」が実務読解の鉄則です。

```text
読む順チェックリスト
1. backend  : state はどこか(このコードの守備範囲)
2. provider : どのクラウド・リージョン・アカウントか
3. variables: 何が環境ごとに変わるのか
4. main     : 実際に何を作っているのか
```

# Lesson 12 state・バックエンド・プロバイダ

Terraform を実行する「土台」を読めるようになるレッスンです。state(実リソースとの対応表)、backend(state の保存先)、プロバイダのバージョン制約と alias を、実務コードの読解を中心に学びます。演習では読み取ったロジックを locals / output で再現します。

## ch01 stateとは何か

### state とは

**state**(Terraform がコードと実リソースの対応表を保存するファイル。既定では `terraform.tfstate`)は Terraform 運用の心臓部です。lesson01 ch03 で「plan は予告、apply は反映、state は記録」と見ました。このチャプターでは、その記録の中身と扱い方を詳しく見ます。

Terraform は plan のたびに次の3つを比べて差分を計算します。

| 比べるもの | 中身 |
|---|---|
| コード(`.tf`) | こうなっていてほしい、という最終形 |
| state | 前回の apply で「自分が作った・管理している」と記録したもの |
| 実環境 | AWS などに今ある実物(plan の最初に読み直す。これを**リフレッシュ**と呼ぶ) |

AWS には人が手で作ったものや別のチームが作ったものも並んでいます。Terraform が「どれが自分の管理するものか」を知る手がかりは state だけです。

### state の中身をのぞく

サンプルを apply すると、作業フォルダに `terraform.tfstate` ができます。中身は JSON(データを `{ }` と `[ ]` で書くテキスト形式)で、実際の中身の抜粋は次のとおりです(id は `...` に置き換え、一部を省略して1行にまとめています)。

```text
{
  "version": 4,
  "terraform_version": "1.10.1",
  "serial": 3,
  "resources": [
    {
      "mode": "managed",
      "type": "terraform_data",
      "name": "app",
      "instances": [
        {
          "attributes": {
            "id": "...",
            "input":  { "value": "app-server", ... },
            "output": { "value": "app-server", ... }
```

`type`(型)と `name`(名前)の組で「コードのどのリソースか」を、`attributes` で「実物の id や値」を記録しています。`serial` は書き換えのたびに増える通し番号です。

state には実物の値がそのまま入るため、データベースのパスワードなどを扱う構成では**秘密の値が平文(暗号化されていない文字)で残る**ことがあります。state を Git に入れず、暗号化した保存先に置くのはこのためです(保存先は次の ch02)。

### アドレスの読み方

state の中の1件1件は**アドレス**(`型.名前` の形の住所)で呼びます。`terraform state list` はアドレスの一覧を出すコマンドです。サンプルを apply したあとに実行すると次のようになります。

```text
$ terraform state list
terraform_data.app
terraform_data.db
```

count・for_each・モジュールを使うと、アドレスに印が付きます。実際に作って確かめた例です。

```text
$ terraform state list
terraform_data.bucket["assets"]
terraform_data.bucket["logs"]
terraform_data.web[0]
terraform_data.web[1]
module.net.terraform_data.vpc
```

| アドレス | 意味 |
|---|---|
| `terraform_data.web[0]` | count で作った1個目(lesson07。`[番号]` は0から数える) |
| `terraform_data.bucket["logs"]` | for_each のキー `logs` で作ったもの(lesson08) |
| `module.net.terraform_data.vpc` | モジュール `net` の中にある `terraform_data.vpc`(lesson10) |

1件の詳細は `terraform state show アドレス` で見ます。

```text
$ terraform state show 'terraform_data.bucket["logs"]'
# terraform_data.bucket["logs"]:
resource "terraform_data" "bucket" {
    id     = "..."
    input  = "logs"
    output = "logs"
}
```

アドレスに `[ ]` や `"` が入るときは、シェル(コマンドを打つ画面)に記号として解釈されないよう全体を `'...'` で囲みます。

### state を消すとどうなるか

サンプルを apply したあと `terraform.tfstate` を削除して plan すると、実際にこう出ます。

```text
Plan: 2 to add, 0 to change, 0 to destroy.
```

Terraform は作成済みの2つを忘れ、「まだ何もないので2つ作る」と予告しています。本物の AWS なら、同じものがもう1組作られる(二重作成)か、名前が重複して `already exists` のエラーで止まります。どちらにしても、元からある実物は Terraform の管理から外れて放置されます。

手で編集するのも危険です。JSON の書き間違い1つで Terraform が state を読めなくなったり、実物とずれた記録になったりします。state を直す必要があるときは `terraform state mv`(アドレスの付け替え)や `terraform state rm`(管理から外すだけ。実物は消さない)などの専用コマンドを使います。

🟡 「state は消さない・直接編集しない・読むならコマンドで」を必ず押さえましょう。

### 実務の state list を読む

実務の構成で `terraform state list` を実行すると、たとえば次のように並びます。

```text
$ terraform state list
aws_ecs_service.api
aws_iam_role.task
aws_s3_bucket.logs
```

型の先頭 `aws_` は AWS のリソースであることを表します。**ECS**(コンテナ=アプリを箱詰めしたものを動かす AWS のサービス)のサービス `api`、**IAM**(AWS の権限管理の仕組み。lesson13 ch02)のロール `task`、**S3**(ファイル置き場。lesson01)のバケット `logs` の3件を、この構成が管理している、と読めます。一覧はアドレスのアルファベット順に出ます。

### サンプルを1行ずつ

```hcl
resource "terraform_data" "app" {   # アドレス terraform_data.app として state に記録される
  input = "app-server"
}

resource "terraform_data" "db" {    # アドレス terraform_data.db として記録される
  input = "db-server"
}

output "state_addresses" {          # state list で見えるアドレスのイメージを文字列で表示
  value = join(", ", ["terraform_data.app", "terraform_data.db"])  # リストを ", " でつないで1本の文字列に(lesson05)
}

output "managed_count" {            # 管理しているリソースの数
  value = 2
}
```

実行結果です。

```text
managed_count = 2
state_addresses = "terraform_data.app, terraform_data.db"
```

数値の `2` は `"` なし、文字列は `"..."` 付きで表示されます。この講座の「▶ 実行」は毎回新しい空フォルダで動くので、state は実行のたびに作り直されます。

## ch02 backend "s3" の読み方

### バックエンドとは

**バックエンド**(state の保存先の設定)を何も書かないと、state は作業フォルダの `terraform.tfstate` に置かれます。これを **local バックエンド**と呼びます。1人で練習するならこれで足りますが、チームでは困ります。

- state が自分の PC にしかないので、ほかの人が plan すると「何もない」状態から計算してしまう
- PC が壊れたら state も消える(ch01 で見たとおり、管理が外れる)
- 2人が同時に apply すると、state を同時に書き換えて壊してしまう

そこで実務では、state を AWS の **S3**(ファイル置き場のサービス。lesson01)に置き、全員が同じ state を読み書きするのが定番です。

### backend "s3" を1行ずつ読む

典型例です。

```hcl
terraform {                                   # Terraform 自体の設定をまとめるブロック
  backend "s3" {                              # state の保存先を S3 にする
    bucket         = "myapp-tfstate"          # 保存先のバケット名
    key            = "prod/network/terraform.tfstate"  # バケット内のパス(ファイルの置き場所)
    region         = "ap-northeast-1"         # バケットがあるリージョン
    dynamodb_table = "tfstate-lock"           # ロックに使う DynamoDB のテーブル名
  }
}
```

| 引数 | 意味 |
|---|---|
| `bucket` | state を置く S3 バケット。state 専用のバケットを1つ用意することが多い |
| `key` | バケット内のパス。S3 ではファイル1つ1つを**オブジェクト**、その名前を**キー**と呼ぶ。`/` で区切るとフォルダのように見える |
| `region` | **リージョン**(AWS のデータセンターがある地域)。`ap-northeast-1` は東京 |
| `dynamodb_table` | **DynamoDB**(AWS のデータベースサービス)のテーブル。ロックの記録に使う |

`terraform` ブロック(lesson01 で見た `resource` などとは別の、Terraform 自体の設定を書くブロック)の中に `backend` を書く、という入れ子の形です。`backend` のラベル `"s3"` が保存先の種類です。

### key の命名から構成の分け方を読む

key は「環境/コンポーネント/terraform.tfstate」で切る命名が多く、ここを見るとその構成がどの単位で分割されているかが分かります。たとえば同じバケットに次の key が並んでいれば、

| key | 読み取れること |
|---|---|
| `prod/network/terraform.tfstate` | 本番環境のネットワーク部分 |
| `prod/app/terraform.tfstate` | 本番環境のアプリ部分 |
| `stg/network/terraform.tfstate` | 検証環境(stg)のネットワーク部分 |

「環境ごと(lesson11)、さらにネットワークとアプリで state を分けている」と分かります。state を分けると、1回の plan の範囲が狭くなり、アプリの変更でネットワークを壊す心配が減ります。

### ロックとは

**ロック**(同時 apply による state 破損を防ぐ排他制御)は、apply を始めた人が「今使用中」という印を付け、終わるまでほかの人の apply を止める仕組みです。local バックエンドにもロックはあり、1つ目の apply 中に同じフォルダで2つ目を実行したところ、実際に次のエラーで止まりました(抜粋。Who は伏せています)。

```text
Error: Error acquiring the state lock

Lock Info:
  ID:        ...
  Path:      terraform.tfstate
  Operation: OperationTypeApply
  Who:       ...
  Version:   1.10.1
```

`Error acquiring the state lock` は「ロックを取れなかった(ほかの誰かが使用中)」という意味です。S3 バックエンドでは、この印を DynamoDB のテーブルに書くのが長く定番でした。Terraform 1.10 からは `use_lockfile = true` と書くと S3 だけでロックできる方式も加わったので、新しめのコードではこちらを見かけることもあります。

### backend には変数が使えない

key を `"${var.env}/network/terraform.tfstate"` のように変数で組み立てたくなりますが、backend ブロックでは変数が使えません。実際に試すと、init の時点で次のエラーになります。

```text
Error: Variables not allowed

  on main.tf line 5, in terraform:
   5:     key    = "${var.env}/network/terraform.tfstate"

Variables may not be used here.
```

backend は「state をどこから読むか」を決める設定なので、変数より先に決まっている必要があるからです。そのため実務の backend は値が**直書き**されているのが普通で、環境ごとにフォルダを分けて別々の backend を書くか、`terraform init -backend-config=...` で外から値を渡します。

🟡 backend を見たら「どこに(bucket・region)・どのパスで(key)・ロックは何か(dynamodb_table / use_lockfile)」の3点を読み取りましょう。

### サンプルを1行ずつ

サンプルは backend そのものではなく、key の組み立てルールだけを locals で再現します(この講座は AWS につながないため)。

```hcl
variable "env" {          # 環境名の入力口(lesson03)
  default = "stg"
}

variable "component" {    # コンポーネント名の入力口
  default = "app"
}

locals {
  state_key = "${var.env}/${var.component}/terraform.tfstate"  # ${ } は文字列の中に値を埋め込む書き方(lesson04)
}

output "state_key" {
  value = local.state_key
}
```

実行結果です。

```text
state_key = "stg/app/terraform.tfstate"
```

## ch03 required_providersとバージョン制約

### プロバイダとは

**プロバイダ**(Terraform が AWS などを操作するためのプラグイン)は、lesson01 ch03 で「init のときにダウンロードされるもの」として名前だけ出てきました。Terraform 本体は AWS のことを何も知りません。`aws_s3_bucket` のような `aws_` で始まる型は、AWS プロバイダが提供していて、プロバイダが AWS の API(プログラムから AWS を操作するための窓口)を呼んで実物を作ります。この講座で使っている `terraform_data` は Terraform 本体に最初から入っているので、ダウンロード不要でオフラインでも動きます。

### バージョン番号の読み方

プロバイダも Terraform 本体も `5.67.3` のような3つの数字でバージョンを表します。これを**セマンティックバージョニング**(数字の位置に意味を持たせた番号の付け方)と呼びます。

| 位置 | `5.67.3` では | 上がるとき |
|---|---|---|
| メジャー | `5` | 互換性のない大きな変更。今までのコードが動かなくなることがある |
| マイナー | `67` | 機能の追加。今までのコードはそのまま動く想定 |
| パッチ | `3` | バグ修正だけ |

メジャーが上がると、引数の名前が変わったり廃止されたりして、plan がエラーになったり想定外の変更が出たりします。それを防ぐために、使ってよいバージョンの範囲を**バージョン制約**として書いておきます。

### required_providers を1行ずつ読む

```hcl
terraform {                              # Terraform 自体の設定(ch02 の backend と同じブロック)
  required_version = ">= 1.5.0"          # Terraform 本体は 1.5.0 以上が必要
  required_providers {                   # 使うプロバイダの一覧
    aws = {                              # このコードの中で aws という名前で使うプロバイダ
      source  = "hashicorp/aws"          # 入手元。「配布元/名前」の形
      version = "~> 5.67"                # 使ってよいバージョンの範囲
    }
  }
}
```

- `required_version`: Terraform 本体のバージョン制約
- `required_providers`: 使うプロバイダの**入手元とバージョン制約の宣言**
- `aws = { ... }`: `=` の右の `{ }` は、`source` と `version` という2つの値をまとめたオブジェクトです(lesson04 の map と同じ書き方)
- `source = "hashicorp/aws"`: Terraform Registry(プロバイダの公開置き場)の `hashicorp` が配布している `aws` プロバイダ、という意味です

init はこの制約を満たすバージョンを選んでダウンロードし、選んだバージョンを `.terraform.lock.hcl`(ロックファイル)に記録します。次からはそのバージョンが使われるので、人によってバージョンがずれることを防げます。新しいバージョンに上げたいときは `terraform init -upgrade` を実行します。

### 制約の記号

| 書き方 | 許す範囲 |
|---|---|
| `= 5.67.3`(または `5.67.3`) | そのバージョンだけ(完全固定) |
| `>= 1.5.0` | 1.5.0 以上。上限なし |
| `>= 1.5.0, < 2.0.0` | `,` で条件を並べると「両方を満たす」範囲 |
| `~> 5.67` | 5.67 以上 6.0 未満 |
| `~> 5.67.0` | 5.67.0 以上 5.68.0 未満 |

`>=` は下限だけの指定です。`~>`(悲観的制約)は「最後に書いた桁だけ上げてよい」という意味で、`~> 5.67` は最後の桁 `67`(マイナー)だけ上げてよいので 5.67 以上 6.0 未満、`~> 5.67.0` なら最後の桁(パッチ)だけ上げてよいので 5.67.x のパッチ更新のみ許可です。メジャーバージョンアップ事故を防ぐため、実務ではほぼ `~>` が使われます。

Terraform v1.10.1 で `required_version` を変えて init を試すと、`"~> 1.10.0"`・`"~> 1.5"`・`">= 1.5.0, < 2.0.0"` は通り、`"~> 1.9.0"`(1.9.x のみ)は通りませんでした。制約を満たさないときは次のエラーで止まります(抜粋)。

```text
Error: Unsupported Terraform Core version

  on main.tf line 2, in terraform:
   2:   required_version = "~> 1.9.0"

This configuration does not support Terraform version 1.10.1. To proceed,
```

「この構成は Terraform 1.10.1 に対応していない」という意味です。

🟡 `~>` がどの範囲までの更新を許すかを読めるようにしましょう。

### サンプルを1行ずつ

```hcl
locals {
  constraints = {                                                   # 制約 → 意味 の対応表(map)
    "~> 5.67"   = "5.67 以上 6.0 未満(マイナー更新まで許可)"
    "~> 5.67.0" = "5.67.0 以上 5.68.0 未満(パッチ更新のみ許可)"
    ">= 1.5.0"  = "1.5.0 以上なら何でもよい(上限なし)"
  }
}

output "pessimistic_minor" {
  value = local.constraints["~> 5.67"]    # map["キー"] でキーに対応する値を取り出す
}

output "lower_bound_only" {
  value = local.constraints[">= 1.5.0"]
}
```

map のキーに空白や記号が入るときは、キーを `"..."` で囲みます。実行結果です(名前のアルファベット順)。

```text
lower_bound_only = "1.5.0 以上なら何でもよい(上限なし)"
pessimistic_minor = "5.67 以上 6.0 未満(マイナー更新まで許可)"
```

## ch04 provider alias

### provider ブロックとは

ch03 の `required_providers` は「どのプロバイダを使うか」の宣言でした。それとは別に、**provider ブロック**で「そのプロバイダをどの設定で使うか」を書きます。AWS プロバイダで一番大事な設定は `region`(リージョン。AWS のデータセンターがある地域)です。

| リージョン名 | 場所 |
|---|---|
| `ap-northeast-1` | 東京 |
| `ap-northeast-3` | 大阪 |
| `us-east-1` | 米国バージニア北部 |

```hcl
provider "aws" {             # aws プロバイダの設定(ラベルはプロバイダ名1つ)
  region = "ap-northeast-1"  # この設定で作るリソースは東京に置かれる
}
```

ふつうは provider ブロックが1つだけで、すべての `aws_` リソースがこの設定(東京)で作られます。

### alias で設定を複数持つ

**alias**(同じプロバイダに複数の設定を持たせるときの名前)は、マルチリージョン(複数の地域にまたがる構成)やマルチアカウント(複数の AWS アカウントにまたがる構成)で登場します。

```hcl
provider "aws" {                 # alias なし = 既定の設定
  region = "ap-northeast-1"
}

provider "aws" {                 # 2つ目の aws 設定
  alias  = "virginia"            # この設定の呼び名
  region = "us-east-1"
}

resource "aws_acm_certificate" "cdn" {
  provider    = aws.virginia     # この1つだけ virginia の設定で作る
  domain_name = "cdn.example.com"
}
```

1行ずつの意味です。

| 行 | 意味 |
|---|---|
| `alias = "virginia"` | 2つ目の設定に `virginia` という名前を付ける。alias のない設定が既定になる |
| `aws_acm_certificate` | **ACM**(SSL/TLS 証明書=https 通信に使う電子証明書を発行・管理する AWS のサービス)の証明書 |
| `provider = aws.virginia` | 「プロバイダ名.alias」の形で、使う設定を指定する。`"..."` で囲まない |
| `domain_name` | 証明書を発行する対象のドメイン名(`example.com` は例示用に予約された名前) |

なぜここだけバージニアなのかというと、**CloudFront**(世界中の拠点からコンテンツを配信する AWS のサービス)で使う ACM 証明書は us-east-1 に作る決まりがあるからです。アプリ本体は東京、証明書だけバージニア、という構成でこの書き方がよく出ます。

`provider = aws.virginia` の付いたリソースだけが別リージョン(マルチアカウントなら別アカウント)に作られます。`provider =` が書かれていないリソースは、すべて alias なしの既定の設定で作られます。

### マルチアカウントとモジュールでの見え方

マルチアカウントの場合は、alias 付きの provider の中に `assume_role` ブロック(別アカウントの権限を借りる設定)が入ります。その中には借りるロールの **ARN**(AWS のリソースを一意に指す名前。lesson13 ch02)を書きます。alias ごとに「どのリージョン・どのアカウントか」が決まる、という読み方は同じです。

モジュール(lesson10)を呼ぶ側では、次の形で alias を渡すことがあります。

```hcl
module "cdn" {
  source = "./modules/cdn"
  providers = {
    aws = aws.virginia   # モジュールの中の aws は、呼び出し側の aws.virginia の設定を使う
  }
}
```

⚪ resource 内に `provider =` を見つけたら「どの alias の設定で作られるか」を provider ブロックまで遡って確認する、という読み方だけ覚えておけば十分です。

### サンプルを1行ずつ

サンプルは AWS につながずに、alias とリージョンの対応だけを map で整理します。

```hcl
locals {
  provider_regions = {           # alias → リージョン の対応表(map)
    default  = "ap-northeast-1"  # alias なしの設定は default というキーで表す
    virginia = "us-east-1"
  }
}

output "default_region" {
  value = local.provider_regions["default"]   # map から default の値を取り出す
}

output "virginia_region" {
  value = local.provider_regions["virginia"]
}
```

実行結果です。

```text
default_region = "ap-northeast-1"
virginia_region = "us-east-1"
```

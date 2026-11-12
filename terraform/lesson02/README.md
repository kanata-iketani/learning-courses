# Lesson 02 resourceと参照

Terraform の中心である resource ブロックと、リソース同士を「参照」でつなぐ書き方を学ぶレッスンです。演習はクラウド不要の `terraform_data` で行い、実務の AWS リソースや data ソースのコードは読解例として登場します。

## ch01 resourceの基本形とterraform_data

### resource の基本形

**resource**(Terraform に作らせたいものを宣言するブロック)は `resource "型" "名前" { 引数 }` が基本形です。lesson01 ch02 で見た「種別 + ラベル2つ + 本体」の形そのものです。

| 部品 | 例 | 意味 |
|---|---|---|
| `resource` | | 「管理したいものを1つ定義します」という種別 |
| 型(1つ目のラベル) | `"terraform_data"`、`"aws_s3_bucket"` | 何を作るか。種類はプロバイダごとに決まっている |
| 名前(2つ目のラベル) | `"server"` | コードの中でこのリソースを呼ぶための名前 |
| 本体 `{ }` | `input = "practice"` | 設定(引数)を `名前 = 式` で書く |

🔴 resource の基本形は実務コードの大半を占めるので、手が覚えるまで書きましょう。

### 型は「プロバイダ名_リソース種類」

型は「**プロバイダ名**_リソース種類」の形をしています。プロバイダは lesson01 ch03 で見た「AWS などを操作するためのプラグイン」です。先頭の `aws_` を見れば AWS 用、残りを見れば何のサービスかが分かります。

| 型 | プロバイダ | 作るもの |
|---|---|---|
| `aws_s3_bucket` | aws | S3 バケット(ファイル置き場) |
| `aws_instance` | aws | **EC2** インスタンス(AWS で借りる仮想サーバー1台) |
| `aws_vpc` | aws | **VPC**(AWS 上に作る自分専用のネットワーク。ch02・ch03 で詳しく) |
| `terraform_data` | terraform(組み込み) | 何も作らない練習用のリソース |

`terraform_data` だけは `aws_` のような接頭辞がありません。Terraform 本体に組み込まれているので、プロバイダのダウンロードもクラウドのアカウントも不要です。

### 名前はコードの中だけの識別子

名前(`"server"` など)は、コードの中で「どのリソースか」を区別するためだけのものです。AWS 上に作られるものの名前とは別物です(S3 バケットの実際の名前は、本体の `bucket = "..."` のような引数で決めます)。

同じ型の中で同じ名前を2回使うとエラーになります。

```text
Error: Duplicate resource "terraform_data" configuration
...
A terraform_data resource named "server" was already declared at
main.tf:1,1-35. Resource names must be unique per type in each module.
```

「型ごとに名前は1つだけ」という意味です。型が違えば同じ名前(例: `aws_vpc.main` と `aws_subnet.main`)を使えます。

注意したいのは、**名前を変えると Terraform は「別のリソース」とみなす**ことです。サンプルを apply したあと、名前を `server` から `web` に書き換えて plan すると、次の予告になりました。

```text
  # terraform_data.server will be destroyed
  # (because terraform_data.server is not in configuration)
  - resource "terraform_data" "server" {
      - id     = "..." -> null
      ...
    }

  # terraform_data.web will be created
  + resource "terraform_data" "web" {
      ...
    }

Plan: 1 to add, 0 to change, 1 to destroy.
```

「`server` はコードから消えたので削除、`web` は新しいので作成」という扱いです(`-> null` は「値がなくなる」の意味)。本物のサーバーなら作り直しになるので、実務では名前を気軽に変えません。

### 引数と属性

- **引数**(argument): 本体に自分で書く設定。`terraform_data` なら `input`
- **属性**(attribute): リソースが持っていて、外から読める値。`terraform_data` なら `id`、`input`、`output`

`terraform_data` は、引数 `input` に入れた値を apply 後に属性 `output` としてそのまま持ちます。`id` は Terraform が付ける識別番号(UUID という長いランダムな文字列)です。引数として書いた `input` も属性として読めるので、`terraform_data.server.input` でも同じ値が取れます。この講座では「apply 後に決まる値」の練習として `output` 属性を使います。

### サンプルを1行ずつ

```hcl
resource "terraform_data" "server" {   # 型 terraform_data、名前 server のリソース
  input = "practice"                   # 引数 input に文字列 "practice"
}

output "server_value" {                 # output(結果表示)server_value
  value = terraform_data.server.output  # server リソースの output 属性(型.名前.属性。ch02)
}

output "resource_type" {                # output resource_type
  value = "terraform_data"              # 文字列をそのまま表示
}
```

plan の予告(抜粋)です。

```text
  # terraform_data.server will be created
  + resource "terraform_data" "server" {
      + id     = (known after apply)
      + input  = "practice"
      + output = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + resource_type = "terraform_data"
  + server_value  = (known after apply)
```

`# terraform_data.server` のように、plan はリソースを「型.名前」で表示します。`input` は書いた値なので最初から分かっていますが、`id` と `output` は apply してから決まるので `(known after apply)` です。

apply 後の output(名前のアルファベット順):

```text
resource_type = "terraform_data"
server_value = "practice"
```

### 実務の読解例: EC2

実務ではこう書かれることが多いです。

```hcl
resource "aws_instance" "web" {    # 型 aws_instance(EC2)、名前 web
  ami           = "ami-12345678"   # 起動に使う AMI の ID
  instance_type = "t3.micro"       # サーバーの大きさ(CPU・メモリ)
}
```

- `ami`: **AMI**(Amazon Machine Image。OS などが入ったサーバーのひな形)の ID。`ami-` で始まる文字列です
- `instance_type`: サーバーの性能の種類。`t3.micro` は小さめ(安価)な種類の1つです
- `=` の位置がそろっているのは、`terraform fmt`(コードの書式を自動で整えるコマンド)が縦にそろえるためです。意味はありません

この3行で「`t3.micro` の大きさで、`ami-12345678` から起動した仮想サーバーが1台ある状態」を宣言しています。コードの中では `aws_instance.web` と呼びます。

## ch02 リソース参照 型.名前.属性

### 参照とは

あるリソースの値は `型.名前.属性`(例: `terraform_data.origin.output`)で**参照**(他のブロックの値を式の中で使うこと)できます。`=` の右側(式)に書きます。

```hcl
value = terraform_data.origin.output
```

`.`(ドット)は「〜の中の」と読みます。

| 部分 | 意味 |
|---|---|
| `terraform_data` | 型 |
| `.origin` | その型の中の、名前が origin のリソース |
| `.output` | そのリソースの中の、output 属性 |

つまり「terraform_data 型の origin というリソースの output 属性の値」です。属性は ch01 で見た「リソースが持っていて外から読める値」です。

🔴 参照の形は読解の要なので、手が覚えるまで書きましょう。

### 参照すると依存関係ができる

参照を書くと Terraform は**依存関係**(どちらを先に作るべきかの順序)を自動で認識し、参照先を先に作成します。値を使う側は、参照先ができあがって値が決まるまで作れないからです。順序を手で書く必要はありません。

Terraform はファイルに書いた順番では動きません。コード全体を読んで参照をたどり、「先に作るべきもの」から順に作ります。参照のないもの同士は、順不同(同時に作ることもある)です。

### リテラルと参照の違い

サンプルでは、同じ文字列 `"origin-value"` を2通りで表示しています。

```hcl
resource "terraform_data" "origin" {      # 参照される側のリソース
  input = "origin-value"
}

output "from_resource" {
  value = terraform_data.origin.output    # 参照: origin の output 属性を使う
}

output "from_literal" {
  value = "origin-value"                  # リテラル: 文字をそのまま書いただけ
}
```

plan の予告(抜粋)を見ると違いが分かります。

```text
Changes to Outputs:
  + from_literal  = "origin-value"
  + from_resource = (known after apply)
```

- `from_literal` は書いたとおりの値なので、plan の時点で決まっています
- `from_resource` は origin の `output` 属性を参照しているので、origin が作られる(apply)まで値が分かりません

apply 後はどちらも同じ値になります。

```text
from_literal = "origin-value"
from_resource = "origin-value"
```

結果が同じでも意味は違います。origin の `input` を書き換えると `from_resource` はそれに合わせて変わりますが、`from_literal` は変わりません。同じ値を2か所に書くより、参照で1か所から持ってくるほうが、書き換え漏れが起きません。

### 存在しないものを参照するとエラー

参照先の名前を書き間違えると(`origin` を `orign` と書いたとき)、plan の段階でエラーになります。

```text
Error: Reference to undeclared resource

  on main.tf line 2, in output "x":
   2:   value = terraform_data.orign.output

A managed resource "terraform_data" "orign" has not been declared in the root
module.
```

「`terraform_data` 型の `orign` というリソースは宣言されていない」という意味です。`on main.tf line 2` でエラーの場所(ファイル名と行番号)が分かります。

### 実務の読解例: VPC とサブネット

実務コードでは `vpc_id = aws_vpc.main.id` のような参照が至るところに出てきます。

```hcl
resource "aws_subnet" "app" {   # 型 aws_subnet(サブネット)、名前 app
  vpc_id = aws_vpc.main.id      # aws_vpc 型の main の id 属性 → VPC が先に作られる
}
```

- **VPC**: AWS 上に作る自分専用のネットワーク
- **サブネット**: VPC の中をさらに区切った小さなネットワーク。サーバーはサブネットの中に置く
- `vpc_id`: 「このサブネットをどの VPC の中に作るか」を指定する引数
- `aws_vpc.main.id`: 別の場所で定義した `resource "aws_vpc" "main"` の `id` 属性。`id` は AWS が付ける ID(`vpc-` で始まる文字列)で、VPC を作るまで分かりません

VPC の ID は作ってみるまで分からないので、コードに直接書くことはできません。そこで参照を使い、「main という VPC の ID を入れる」と書きます。Terraform は参照を見て VPC → サブネットの順に作り、できあがった VPC の ID をサブネットに渡します。

読むときは「`=` の右に `型.名前.属性` があれば、別リソースへの依存」と読めるようになるのが目標です。

## ch03 複数リソースのチェーン

### 参照は何段でもつなげられる

参照は何段でもつなげられます。B が A を参照し、C が B を参照すれば、作成順は自動的に A → B → C になります。このつながりを**参照のチェーン**(鎖)と呼びます。

この講座では `terraform_data` の `input` に別リソースの `output` 属性を渡してチェーンを作ります。

🔴 参照をつないで依存の流れを作る感覚を、手が覚えるまで書きましょう。

### サンプルを1行ずつ

```hcl
resource "terraform_data" "base" {        # 1段目: base
  input = "base-v1"                       # 文字列をそのまま入れる
}

resource "terraform_data" "middle" {      # 2段目: middle
  input = terraform_data.base.output      # base の output を input に入れる → base が先
}

resource "terraform_data" "last" {        # 3段目: last
  input = terraform_data.middle.output    # middle の output を input に入れる → middle が先
}

output "chain_result" {
  value = terraform_data.last.output      # 最後の last の output を表示
}
```

`"base-v1"` という値が base → middle → last と受け渡されていきます。

| リソース | input | output |
|---|---|---|
| base | `"base-v1"`(リテラル) | `"base-v1"` |
| middle | base の output | `"base-v1"` |
| last | middle の output | `"base-v1"` |

### 実際の作成順

plan の予告では、リソースは名前のアルファベット順(base → last → middle)に並びます。表示の順番であって、作る順番ではありません。

```text
  # terraform_data.base will be created
  + resource "terraform_data" "base" {
      + input  = "base-v1"
      ...
  # terraform_data.last will be created
  + resource "terraform_data" "last" {
      + input  = (known after apply)
      ...
  # terraform_data.middle will be created
  + resource "terraform_data" "middle" {
      + input  = (known after apply)
      ...
Plan: 3 to add, 0 to change, 0 to destroy.
```

middle と last の `input` が `(known after apply)` になっているのは、参照先がまだ作られていないからです。

apply すると、参照をたどった順番どおりに作られます。

```text
terraform_data.base: Creating...
terraform_data.base: Creation complete after 0s [id=...]
terraform_data.middle: Creating...
terraform_data.middle: Creation complete after 0s [id=...]
terraform_data.last: Creating...
terraform_data.last: Creation complete after 0s [id=...]

Apply complete! Resources: 3 added, 0 changed, 0 destroyed.
```

output は次のとおりです。

```text
chain_result = "base-v1"
```

### 元の値を変えると、つながった先も変わる

apply したあとに base の `input` を `"base-v2"` に書き換えて、もう一度 apply しました。

```text
  # terraform_data.base will be updated in-place
  ~ resource "terraform_data" "base" {
      ~ input  = "base-v1" -> "base-v2"
      ~ output = "base-v1" -> (known after apply)
    }

  # terraform_data.last will be updated in-place
  ~ resource "terraform_data" "last" {
      ~ input  = "base-v1" -> (known after apply)
      ...
  # terraform_data.middle will be updated in-place
  ~ resource "terraform_data" "middle" {
      ~ input  = "base-v1" -> (known after apply)
      ...
Plan: 0 to add, 3 to change, 0 to destroy.
```

書き換えたのは base の1行だけですが、参照でつながった middle と last も変更対象になりました(`~` は lesson01 ch03 で見た「その場で変更」の印)。変更も base → middle → last の順に行われ、結果は `chain_result = "base-v2"` になります。

### 実務の読解例: VPC → サブネット → EC2

実務の AWS コードは、このような参照のチェーンでできています。

```hcl
resource "aws_vpc" "main" { cidr_block = "10.0.0.0/16" }   # 1. ネットワーク(VPC)

resource "aws_subnet" "app" {
  vpc_id = aws_vpc.main.id        # 2. VPC の中にサブネット(VPC → サブネット)
}

resource "aws_instance" "web" {
  subnet_id = aws_subnet.app.id   # 3. サブネットの中に EC2(サブネット → EC2)
}
```

- 1行目は `{ }` の中身が1つだけなので1行にまとめて書いています。改行した形と意味は同じです
- `cidr_block`: VPC で使う IP アドレスの範囲。**CIDR**(サイダー)は `10.0.0.0/16` のように「先頭のアドレス/固定する桁数」で範囲を表す書き方です。`/16` は先頭16ビット(`10.0` の部分)が固定で、`10.0.0.0`〜`10.0.255.255` の約6.5万個のアドレスを使えるという意味です
- `subnet_id`: EC2 をどのサブネットに置くかを指定する引数
- ch01・ch02 で見たとおり、VPC はネットワーク、サブネットはその中の区画、EC2 は仮想サーバーです

参照をたどると `aws_instance.web` → `aws_subnet.app` → `aws_vpc.main` とつながっているので、作る順は VPC → サブネット → EC2 です。実務コードを読むときは「`=` の右辺の参照をたどって依存の連鎖を追う」のが基本の読み方です。ファイルの中で離れた場所に書かれていても、参照があればつながっています。

## ch04 dataソースの読み方

### data ソースとは

実務コードには `resource` のほかに `data` で始まるブロックもよく出てきます。**data ソース**(既存のものを作らずに「読むだけ」のブロック)です。

- `resource`: Terraform が**作って管理する**もの。コードから消せば削除される
- `data`: すでにどこかにあるものを**探して読む**だけ。作らないし、消しもしない

たとえば「ネットワーク(VPC)は別のチームがすでに作ってある。自分たちはその中にサーバーを置きたい」という場面では、VPC を `resource` で書くと新しく作ってしまいます。そこで `data` で既存の VPC を探し、その ID を読んで使います。

🟡 data を見たら「作らずに読んでいる」と分かれば十分です。

### 書き方と参照の形

```hcl
data "型" "名前" {
  検索条件
}
```

形は resource と同じ「種別 + ラベル2つ + 本体」ですが、本体には作るための設定ではなく「何を探すか」の条件を書きます。

参照は先頭に `data.` を付けて `data.型.名前.属性` とします。

| ブロック | 参照の形 | 例 |
|---|---|---|
| `resource "aws_vpc" "main"` | `型.名前.属性` | `aws_vpc.main.id` |
| `data "aws_vpc" "existing"` | `data.型.名前.属性` | `data.aws_vpc.existing.id` |

実務コードで `data.` から始まる参照を見たら「既存のものから読んだ値」です。

### 実務の読解例: 既存 VPC を探して使う

```hcl
data "aws_vpc" "existing" {          # aws_vpc 型の data ソース。名前は existing
  tags = { Name = "main-vpc" }       # 検索条件: Name タグが main-vpc の VPC
}

resource "aws_subnet" "app" {        # サブネットは新しく作る
  vpc_id = data.aws_vpc.existing.id  # 読んできた VPC の id を使う(data. で始まる)
}
```

- **タグ**: AWS のリソースに付けられる「キー = 値」のラベル。`Name` タグはコンソールに表示される名前としてよく使われます
- `{ Name = "main-vpc" }`: `{ }` で「キー = 値」の組をまとめた値です(lesson03 ch02 で見る map)。ここでは「キー Name、値 main-vpc」の1組です
- 全体で「Name タグが main-vpc の VPC を AWS から探して、その ID を新しいサブネットに使う」という意味です

data ソースは通常 plan のときに読みにいくので、参照する側(サブネット)より先に値が分かります。

### 実務でよく見る data ソース

| data ソース | 何を読むか |
|---|---|
| `data "aws_vpc"` | 既存の VPC(ネットワーク) |
| `data "aws_ami"` | 条件に合う AMI(サーバーのひな形。lesson02 ch01)。「最新の Amazon Linux」を探すのによく使う |
| `data "aws_caller_identity" "current"` | いま Terraform を実行している AWS アカウントの情報。`data.aws_caller_identity.current.account_id` で12桁のアカウント ID が取れる |

`aws_caller_identity` は検索条件がないので、本体は `{}` と空で書かれます。

### data ソースを実行したときの表示

AWS を使わずに動かせる data ソースもあります。`terraform_remote_state`(別の Terraform の state から output を読む data ソース。lesson12 で扱います)を使い、隣のフォルダで apply 済みの output `ami_id` を読む例を実際に動かしました。

```hcl
data "terraform_remote_state" "shared" {
  backend = "local"                                     # state はローカルのファイル
  config = {
    path = "../other/terraform.tfstate"                 # 読む state ファイルの場所
  }
}

output "ami_from_data" {
  value = data.terraform_remote_state.shared.outputs.ami_id   # data. で始まる参照
}
```

apply の表示は次のとおりです。

```text
data.terraform_remote_state.shared: Reading...
data.terraform_remote_state.shared: Read complete after 0s

Changes to Outputs:
  + ami_from_data = "ami-12345678"
...
Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
```

`Reading...` / `Read complete` が「読んだ」という表示です。resource のときの `Creating...` は出ず、`0 added` のとおり何も作られていません。

### この講座のサンプルと演習

`▶ 実行` の環境では外部の値を用意できないので、演習は `terraform_data` で「よそで用意された値を参照して使う」構図だけを再現します。

```hcl
resource "terraform_data" "registry" {      # 「既存の共有値」に見立てたリソース
  input = "shared-config-v2"
}

resource "terraform_data" "consumer" {      # 値を使う側
  input = terraform_data.registry.output    # registry の値を読んで使う
}

output "consumed" {
  value = terraform_data.consumer.output
}

output "verb" {
  value = "read-only"
}
```

ここでの registry は本当は resource(作るもの)なので、data ソースそのものではありません。「値を持っている側」と「それを参照して使う側」という関係だけを練習しています。実行結果は次のとおりです。

```text
consumed = "shared-config-v2"
verb = "read-only"
```

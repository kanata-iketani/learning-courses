# Lesson 13 実務コード読解1：AWS典型パターン

ここからが講座の核心です。実務の AWS コードに繰り返し現れる型 — name_prefix とタグの merge、IAM ポリシーの2流儀、セキュリティグループの ingress 生成、変数駆動の度合い — を読み解き、演習でロジックを再現します。

## ch01 命名とタグの流儀

### このレッスンで読むもの

lesson13 では、実務の AWS の Terraform コードに繰り返し出てくる型を読みます。AWS のリソースはこの講座では動かせないので、本文で「そのリソースが何か」と「コードの1行ずつの意味」を説明し、サンプルと演習では同じロジックを `locals` と `output` で再現して確かめます。

### リソース名とタグとは

AWS のリソースには、たいてい2種類の目印を付けます。

- **リソース名**: S3 バケット名(lesson01)や ECS サービス名など、AWS 上でそのリソースを指す名前。`bucket = ...`、`name = ...` などの引数で指定する
- **タグ**(リソースに付ける `キー = 値` のラベル): 1つのリソースにいくつでも付けられる。管理画面での検索、費用をプロジェクト別・環境別に集計する、といった用途に使う。`Name` というキーのタグは AWS の管理画面の一覧に名前として表示される

ここで出てくる **ECS**(Elastic Container Service。コンテナ=アプリと動作環境を1つの箱にまとめたもの、を動かす AWS のサービス)の**サービス**は、「このアプリを常に何個動かしておく」という単位です。

### name_prefix と common_tags

実務コードの命名は `${var.project}-${var.env}` のような **name_prefix**(リソース名の共通接頭辞)に集約され、タグは `merge()` で「共通タグ + 個別タグ」を合成するのが定番です。

```hcl
locals {
  name_prefix = "${var.project}-${var.env}"   # 例: project="app", env="dev" なら "app-dev"
  common_tags = {                             # 全リソースに付ける共通タグ(map)
    Project   = var.project                   # どのプロジェクトか
    Env       = var.env                       # どの環境か(dev / stg / prod など。lesson11)
    ManagedBy = "terraform"                   # Terraform で管理していることの印
  }
}

resource "aws_s3_bucket" "logs" {
  bucket = "${local.name_prefix}-logs"        # バケット名 "app-dev-logs"
  tags   = merge(local.common_tags, { Name = "${local.name_prefix}-logs" })  # 共通タグ + Name タグ
}
```

| 書き方 | 意味 |
|---|---|
| `"${var.project}-${var.env}"` | 文字列の中に `${ }` で値を埋め込む(lesson04)。`-` はただの文字 |
| `common_tags = { ... }` | `キー = 値` を並べた map(lesson04) |
| `tags = ...` | AWS リソースのタグを指定する引数。値は map |
| `merge(A, B)` | map A と map B を1つにまとめる(lesson05) |
| `{ Name = "..." }` | その場で書いた、キーが1つだけの map |

こうしておくと、全リソースの名前が `app-dev-` で始まり、全リソースに同じ3つのタグが付きます。env を `prod` にするだけで、名前もタグも本番用にそろって切り替わります。

### merge は後の引数が勝つ

`merge` は同じキーがあると後の引数が勝ちます。共通タグにも `Name` が入っている場合で試すと、実際に次のようになりました。

```hcl
locals {
  common_tags = { Env = "dev", Name = "common" }
}
output "merged" {
  value = merge(local.common_tags, { Name = "app-dev-logs" })
}
```

```text
merged = {
  "Env" = "dev"
  "Name" = "app-dev-logs"
}
```

`Name` は後ろの map の値 `app-dev-logs` で上書きされ、`Env` はそのまま残っています。

🔴 「locals に共通部品を置き、resource 側で merge して個別化する」流れは実務コードの至る所に出るので、必ず追えるようにしましょう。

### jsonencode で map を1行の文字列にする

サンプルではタグの map を `jsonencode()`(値を JSON 形式の文字列に変換する関数。lesson05)で文字列にして表示します。JSON に変換すると**キーがアルファベット順に並ぶ**ので、毎回同じ文字列になり、採点で比べやすくなります。

サンプルの実行結果です。

```text
bucket_name = "app-dev-logs"
bucket_tags = "{\"Env\":\"dev\",\"ManagedBy\":\"terraform\",\"Name\":\"app-dev-logs\",\"Project\":\"app\"}"
```

`\"` が多くて読みにくいですが、output は文字列全体を `"..."` で囲んで表示するため、中に含まれる `"` を `\"` と書いて区別しています(**エスケープ**と呼びます)。`\` を取り除くと、中身は次の JSON です。

```text
{"Env":"dev","ManagedBy":"terraform","Name":"app-dev-logs","Project":"app"}
```

`Env`・`ManagedBy`・`Name`・`Project` とアルファベット順に並び、共通タグ3つに `Name` が足されていることが読み取れます。

### サンプルを1行ずつ

```hcl
variable "project" {
  default = "app"
}

variable "env" {
  default = "dev"
}

locals {
  name_prefix = "${var.project}-${var.env}"   # "app-dev"
  common_tags = {
    Project   = var.project
    Env       = var.env
    ManagedBy = "terraform"
  }
}

output "bucket_name" {
  value = "${local.name_prefix}-logs"          # aws_s3_bucket.logs の bucket に入る値
}

output "bucket_tags" {
  value = jsonencode(merge(local.common_tags, { Name = "${local.name_prefix}-logs" }))  # tags に入る値を JSON 文字列で表示
}
```

`jsonencode(merge(...))` のように関数の中に関数があるときは、内側の `merge` が先に計算され、その結果が `jsonencode` に渡ります。

## ch02 IAMポリシーの2流儀

### IAM の基礎の基礎

**IAM**(Identity and Access Management。AWS で「誰が・何に・何をしてよいか」を管理する仕組み)は、実務コードでいちばん多く出てくるものの1つです。AWS は、許可されていない操作はすべて拒否します。そのため、アプリが S3 のファイルを読むだけでも「読んでよい」という許可を書く必要があります。

| 用語 | 意味 |
|---|---|
| **ポリシー** | 許可・拒否のルールを JSON(`{ }` と `[ ]` でデータを書くテキスト形式)で書いた文書 |
| **ロール** | ポリシーをまとめて持つ「権限の入れ物」。ECS で動くアプリなどの AWS サービスが、このロールを借りて操作する |
| **ARN** | Amazon Resource Name。AWS のリソースを一意に指す名前 |

ARN は `arn:aws:サービス:リージョン:アカウントID:リソース` の形です。S3 のバケットは世界で名前が1つしかないので、リージョンとアカウントID を空にして `arn:aws:s3:::app-logs` と書きます(`:::` はこの2つが空という意味)。

| ARN | 指すもの |
|---|---|
| `arn:aws:s3:::app-logs` | バケット `app-logs` そのもの |
| `arn:aws:s3:::app-logs/*` | バケット `app-logs` の中のすべてのファイル(`*` は「何でも」) |

### ポリシーの中身: Effect・Action・Resource

ポリシーの JSON は、ルール1つ1つ(**ステートメント**)のリストでできています。1つのステートメントは次の3点セットです。

| キー | 意味 | 例 |
|---|---|---|
| `Effect` | 許可か拒否か | `"Allow"`(許可)/ `"Deny"`(拒否) |
| `Action` | どの操作を | `"s3:GetObject"`(S3 のファイルを読む)。「サービス名:操作名」の形 |
| `Resource` | どのリソースに対して | ARN で指定する |

先頭の `Version = "2012-10-17"` はポリシーの書式のバージョンを表す決まった文字列で、日付を変える必要はありません。また、`Allow` と `Deny` の両方に当てはまる操作は `Deny` が優先されます。

### 流儀1: jsonencode 直書き

IAM ポリシーの書き方は2流儀に分かれます。流儀1は `jsonencode()`(HCL の値を JSON の文字列に変換する関数。lesson05)で直接書く方法です。

```hcl
resource "aws_iam_role_policy" "read" {       # ロールに直接埋め込むポリシー
  name = "s3-read"                            # ポリシーの名前
  role = aws_iam_role.task.id                 # どのロールに付けるか(別リソースの参照。lesson02)
  policy = jsonencode({                       # ここから下の HCL の値を JSON 文字列にする
    Version = "2012-10-17"                    # 書式のバージョン(決まった値)
    Statement = [{                            # ステートメントのリスト。[ ] の中に { } が1つ
      Effect   = "Allow"                      # 許可する
      Action   = ["s3:GetObject"]             # S3 のファイル読み取りを
      Resource = "arn:aws:s3:::app-logs/*"    # app-logs バケットの中の全ファイルに対して
    }]
  })
}
```

`Statement = [{ ... }]` は「オブジェクト1つだけのリスト」です。ルールを増やすときは `[{ ... }, { ... }]` と並べます。キーが `Effect` のように大文字始まりなのは、AWS のポリシー JSON のキー名をそのまま書いているからです。

### 流儀2: data "aws_iam_policy_document"

流儀2は `data "aws_iam_policy_document"` を使う方法です。**data ブロック**(データソース。何かを作るのではなく、情報を読んだり計算したりして値を返すブロック)の一種で、HCL のブロックでポリシーを組み立て、`.json` 属性で JSON を得ます。

```hcl
data "aws_iam_policy_document" "read" {    # data "型" "名前" { ... }。ラベル2つは resource と同じ
  statement {                              # ステートメント1つ分のブロック
    effect    = "Allow"
    actions   = ["s3:GetObject"]
    resources = ["arn:aws:s3:::app-logs/*"]
  }
}

resource "aws_iam_role_policy" "read" {
  name   = "s3-read"
  role   = aws_iam_role.task.id
  policy = data.aws_iam_policy_document.read.json   # data.型.名前.json で JSON 文字列を参照
}
```

`statement { effect / actions / resources }` と小文字の属性名になり、`actions` `resources` は複数形でリストを取ります。ルールを増やすときは `statement { }` ブロックを並べます。最終的にできる JSON の意味は同じです。

| 流儀2(HCL ブロック) | 流儀1(JSON のキー) |
|---|---|
| `statement { }` | `Statement` のリストの要素 |
| `effect` | `Effect` |
| `actions` | `Action` |
| `resources` | `Resource` |

🔴 見た目が違っても「Effect・Action・Resource の3点セット」を読み取れるようにしましょう。

### サンプルを1行ずつ

サンプルは流儀1のポリシーを locals に置き、`jsonencode` で JSON にします。

```hcl
locals {
  read_policy = {                            # ポリシー全体のオブジェクト
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:GetObject"]
      Resource = "arn:aws:s3:::app-logs/*"
    }]
  }
}

output "policy_json" {
  value = jsonencode(local.read_policy)            # JSON 文字列に変換して表示
}

output "statement_count" {
  value = length(local.read_policy.Statement)      # .Statement でリストを取り出し、要素数を数える
}
```

実行結果です。

```text
policy_json = "{\"Statement\":[{\"Action\":[\"s3:GetObject\"],\"Effect\":\"Allow\",\"Resource\":\"arn:aws:s3:::app-logs/*\"}],\"Version\":\"2012-10-17\"}"
statement_count = 1
```

`\"` は文字列の中の `"` を表すエスケープです(ch01)。`jsonencode` はキーをアルファベット順に並べるので、`Statement` が `Version` より前に、`Action`・`Effect`・`Resource` の順に出ています。

## ch03 セキュリティグループのingress列挙

### 通信の基礎の基礎: IP アドレス・ポート・プロトコル

セキュリティグループを読むには、通信の3つの要素を知っておく必要があります。

| 用語 | 意味 | 例 |
|---|---|---|
| **IP アドレス** | ネットワーク上のコンピューターの住所。0〜255 の数を `.` で4つつないで書く | `10.0.1.25` |
| **ポート** | 1台のコンピューターの中で、どのアプリ宛ての通信かを区別する番号(0〜65535) | 80、443 |
| **プロトコル** | 通信の決まりごと。Web などはほとんど **TCP** | `tcp`、`udp` |

よく見るポート番号は次のとおりです。

| ポート | 用途 |
|---|---|
| 22 | SSH(サーバーにログインして操作する) |
| 80 | HTTP(暗号化しない Web 通信) |
| 443 | HTTPS(暗号化した Web 通信) |
| 5432 | PostgreSQL(データベース) |
| 8080 | アプリの Web サーバーでよく使う番号 |

### CIDR: IP アドレスの範囲の書き方

**CIDR**(サイダー。IP アドレスの範囲を `アドレス/数字` で表す書き方)は、許可する相手をまとめて指定するのに使います。IP アドレスは全部で 32 ビット(0 と 1 が32個)の数で、`/` の後ろの数字は「先頭から何ビットを固定するか」です。固定しない残りのビットは何でもよいので、その分が範囲になります。

| CIDR | 範囲 | アドレスの数 |
|---|---|---|
| `10.0.0.0/8` | `10.` で始まるすべて(10.0.0.0〜10.255.255.255) | 16,777,216 |
| `10.0.0.0/16` | `10.0.` で始まるすべて | 65,536 |
| `10.0.1.0/24` | `10.0.1.` で始まるすべて | 256 |
| `10.0.1.25/32` | `10.0.1.25` の1つだけ | 1 |
| `0.0.0.0/0` | すべてのアドレス(インターネット全体) | 全部 |

`10.` で始まるアドレスは**プライベートアドレス**(社内ネットワークや **VPC**=AWS の中に作る自分専用のネットワーク、の中だけで使う住所)用に予約されています。つまり `10.0.0.0/8` を許可するのは「内部からの通信だけ許可」、`0.0.0.0/0` は「インターネットの誰からでも許可」という意味になります。

### セキュリティグループとは

**セキュリティグループ**(SG。AWS の通信許可ルールの集合)は、サーバーなどに付けて「どの通信を通すか」を決めるものです。lesson09 ch01 で dynamic ブロックの例として登場しました。

- `ingress`(内向きの許可ルール。外からそのサーバーに入ってくる通信)
- `egress`(外向きの許可ルール。そのサーバーから出ていく通信)
- 書けるのは「許可」だけ。どのルールにも当てはまらない通信は通らない
- 入ってきた通信への応答は、egress に書かなくても自動で通る

ingress ブロック1つを1行ずつ読みます。

```hcl
ingress {
  from_port   = 80              # 許可するポート範囲の始まり
  to_port     = 80              # 許可するポート範囲の終わり(同じ値なら 80 番だけ)
  protocol    = "tcp"           # TCP の通信
  cidr_blocks = ["10.0.0.0/8"]  # 相手(送り元)の範囲。リストなので複数書ける
}
```

これで「`10.` で始まるアドレスから、TCP の 80 番ポートへの通信を許可する」という1つのルールになります。`from_port = 1024`、`to_port = 2048` のように違う値を書けば、その間のポートをまとめて許可します。

egress は、出ていく通信をすべて許可する次の形がよく書かれます。`protocol = "-1"` は「すべてのプロトコル」という意味です。Terraform の `aws_security_group` は、egress を書かないと外向きの通信がすべて止まるので、この定型をよく見かけます。

```hcl
egress {
  from_port   = 0
  to_port     = 0
  protocol    = "-1"            # すべてのプロトコル(このときポートは 0 を書く)
  cidr_blocks = ["0.0.0.0/0"]   # どこへでも
}
```

### ベタ書きから dynamic へ

`ingress` には、ベタ書きから `dynamic` + リスト駆動へ移行した痕跡がよく見られます。

```hcl
# 昔: ポートごとにコピペ
ingress {
  from_port   = 80
  to_port     = 80
  protocol    = "tcp"
  cidr_blocks = ["10.0.0.0/8"]
}

# 今: ポートのリストから生成
dynamic "ingress" {                    # ingress ブロックを繰り返し作る(lesson09)
  for_each = var.ingress_ports         # 例: [80, 443] の要素ごとに1つ作る
  content {                            # 1つ分の ingress ブロックの中身
    from_port   = ingress.value        # いま処理中の要素(80、次に 443)
    to_port     = ingress.value
    protocol    = "tcp"
    cidr_blocks = [var.internal_cidr]  # 変数の値を1要素のリストにして渡す
  }
}
```

`var.ingress_ports = [80, 443]` なら、dynamic 版は「80 番の ingress」と「443 番の ingress」の2ブロックをベタ書きしたのと同じ結果になります。ルールの数は元のリストの長さと同じです。

なお、AWS プロバイダの新しめのコードでは、ルールを SG の中に書かず `aws_vpc_security_group_ingress_rule` という別リソースで1ルールずつ書く流儀もあります。見かけたら「ingress ルール1つ分のリソース」と読めば大丈夫です。

🟡 dynamic 版を見たら「for_each の元リストに何が入るか」を variable まで遡り、生成されるルールを数えられるようにしましょう。

### サンプルを1行ずつ

```hcl
variable "ingress_ports" {
  default = [80, 443]                  # 許可したいポートのリスト
}

variable "internal_cidr" {
  default = "10.0.0.0/8"
}

locals {
  rules = [for p in var.ingress_ports : "tcp/${p} from ${var.internal_cidr}"]  # 要素ごとに文字列を作る for 式(lesson06)
}

output "rule_count" {
  value = length(local.rules)          # ルールの数 = リストの長さ
}

output "rules" {
  value = join(", ", local.rules)      # ", " でつないで1本の文字列に
}
```

`[for p in リスト : 式]` は「リストの要素を1つずつ `p` に入れて式を計算し、結果を新しいリストにする」書き方です。dynamic の `ingress.value` が for 式の `p` にあたります。実行結果です。

```text
rule_count = 2
rules = "tcp/80 from 10.0.0.0/8, tcp/443 from 10.0.0.0/8"
```

## ch04 変数駆動の度合いを見抜く

### 題材: ECS のタスク定義

このチャプターの例は **ECS**(コンテナを動かす AWS のサービス。ch01)の**タスク定義**(`aws_ecs_task_definition`。どのコンテナを、どれだけの CPU とメモリで動かすかを決める設計図)です。

| 引数 | 意味 |
|---|---|
| `family` | タスク定義の名前 |
| `cpu` | 割り当てる CPU の量。単位は「1024 = CPU 1個分(1 vCPU)」なので `256` は CPU 4分の1個分 |
| `memory` | 割り当てるメモリの量。単位は MiB(メビバイト。約 1MB)で `1024` は約 1GB |

### 値の出どころは3段階で追う

同じ構成でも「全部 variable 化する派」と「ほぼハードコードする派」がいます。**ハードコード**(値をコードに直接書き込むこと)なら値はその場で分かりますが、variable 化されていると別の場所を見に行く必要があります。設定値の出どころは次の順で追います。

1. resource 内に値が直接書いてあればそこで確定
2. `var.xxx` なら variable ブロックの `default` を見る(lesson03)
3. さらに tfvars やモジュール呼び出しの引数で上書きされていないか確認する

3 の上書きは、次の場所から入ってきます。下にあるものほど優先されます。

| 値の入り口 | 例 |
|---|---|
| variable の `default` | `default = 0` |
| 環境変数 `TF_VAR_名前` | `TF_VAR_container_cpu=512`(シェルで設定する変数) |
| `terraform.tfvars` ファイル | `container_cpu = 512`(lesson03・lesson11) |
| `*.auto.tfvars` ファイル | `prod.auto.tfvars` など |
| コマンドの `-var` / `-var-file` | `terraform apply -var container_cpu=512` |

モジュールの中の `var.xxx` なら、モジュールを呼んでいる側の `module "..." { xxx = ... }` の引数が値の入り口です(lesson10)。

### 3つの書き方を読む

```hcl
# var 派: 値は variable / tfvars を見ないと分からない
cpu = var.container_cpu

# ハードコード派: その場で確定
cpu = 256

# 折衷: 0 (未指定)なら既定値、という条件式もよく見ます
cpu = var.container_cpu > 0 ? var.container_cpu : 256
```

3つ目は**条件式**(`条件 ? 真のときの値 : 偽のときの値`。lesson04)です。

| 部分 | 意味 |
|---|---|
| `var.container_cpu > 0` | 条件。container_cpu が 0 より大きいか |
| `? var.container_cpu` | 条件が true なら、variable の値を使う |
| `: 256` | 条件が false(0 以下)なら 256 を使う |

ここでは `0` を「未指定」の印として使っています。CPU が 0 は実際にはありえない値なので、「0 のままなら既定の 256 にする」という約束です。

🟡 `var.` を見たら default と上書き経路を必ず確認する癖をつけましょう。

### サンプルを1行ずつ

```hcl
variable "container_cpu" {
  default = 0 # 0 は「未指定」の意味で使う流儀
}

locals {
  default_cpu   = 256                                                                # 既定値
  effective_cpu = var.container_cpu > 0 ? var.container_cpu : local.default_cpu      # 実際に使われる値
  cpu_source    = var.container_cpu > 0 ? "variable" : "hardcoded-default"           # 値の出どころを文字で表す
}

output "cpu_source" {
  value = local.cpu_source
}

output "effective_cpu" {
  value = local.effective_cpu
}
```

`locals` の中で別の local(`local.default_cpu`)を参照することもできます。そのまま実行した結果です。

```text
cpu_source = "hardcoded-default"
effective_cpu = 256
```

default が 0 なので条件が false になり、既定値 256 に落ちています。同じフォルダに `container_cpu = 512` と書いた `terraform.tfvars` を置いて実行すると、実際に次のように変わりました。

```text
cpu_source = "variable"
effective_cpu = 512
```

コードは1文字も変えていないのに、tfvars によって結果が変わります。これが「`var.` を見たら default だけで判断せず、上書き経路まで確認する」理由です。
